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
        # Load OpenAI API key
        env_loaded = False
        for path in ['openAI.env', '../openAI.env', './openAI.env']:
            if os.path.exists(path):
                load_dotenv(path)
                env_loaded = True
                logger.info(f"Loaded environment from: {path}")
                break
        
        if not env_loaded or not os.environ.get('openai_apikey'):
            self.stderr.write(self.style.ERROR('OpenAI API key not found'))
            return
            
        client = OpenAI(api_key=os.environ.get('openai_apikey'))
        
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