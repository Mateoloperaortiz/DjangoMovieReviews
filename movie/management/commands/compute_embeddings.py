import os
import numpy as np
from django.core.management.base import BaseCommand
from django.utils import timezone
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv
import logging
import time

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Precompute and store embeddings for all movies'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recomputation of embeddings even if they already exist',
        )

    def handle(self, *args, **options):
        # Attempt to load OpenAI API key from .env files
        # This is primarily for local development. On DO, these files won't exist.
        env_loaded_from_file = False
        for path in ['openAI.env', '../openAI.env', './openAI.env']:
            if os.path.exists(path):
                load_dotenv(path)
                env_loaded_from_file = True # Indicates an attempt was made and a file was found
                logger.info(f"Loaded environment variables from: {path}")
                break
        
        # Now, check if the API key is actually available in the environment,
        # either from the .env file (if loaded) or from platform environment variables.
        api_key_value = os.environ.get('openai_apikey')
        
        if not api_key_value:
            # Construct a more informative error message
            error_msg = "OpenAI API key ('openai_apikey') not found. "
            if env_loaded_from_file:
                error_msg += "It was not found in the loaded .env file or as a platform environment variable."
            else:
                error_msg += "No .env file was found, and it was not set as a platform environment variable."
            self.stderr.write(self.style.ERROR(error_msg))
            return
            
        client = OpenAI(api_key=api_key_value)
        
        # Get movies that need embedding computation
        if options['force']:
            movies = Movie.objects.all()
            self.stdout.write(f"Force updating embeddings for all {movies.count()} movies")
        else:
            movies = Movie.objects.filter(embedding__isnull=True)
            self.stdout.write(f"Computing embeddings for {movies.count()} movies without embeddings")
        
        if movies.count() == 0:
            self.stdout.write(self.style.SUCCESS("No movies need embedding updates"))
            return
            
        for i, movie in enumerate(movies):
            if not movie.description:
                self.stdout.write(f"Skipping {movie.title} - no description")
                continue
                
            try:
                # Get embedding for the movie description
                response = client.embeddings.create(input=[movie.description], model="text-embedding-3-small")
                embedding = response.data[0].embedding
                
                # Store the embedding
                movie.embedding = embedding
                movie.embedding_updated_at = timezone.now()
                movie.save()
                
                self.stdout.write(f"[{i+1}/{movies.count()}] Computed embedding for {movie.title}")
                
                # Add rate limit delay to avoid OpenAI API throttling
                time.sleep(0.5)
                
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error computing embedding for {movie.title}: {str(e)}"))
                
        self.stdout.write(self.style.SUCCESS(f"Successfully computed embeddings for {movies.count()} movies"))
