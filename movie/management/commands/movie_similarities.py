import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Calculate similarities between movies using OpenAI embeddings and cosine similarity"

    def add_arguments(self, parser):
        # Add optional arguments for movie titles and prompt
        parser.add_argument('--movie1', type=str, help='Title of the first movie', default="Batman")
        parser.add_argument('--movie2', type=str, help='Title of the second movie', default="Lego Movie")
        parser.add_argument('--prompt', type=str, help='Custom prompt for comparison', 
                            default="superhero movie with action and adventure")

    def handle(self, *args, **options):
        # Get movie titles and prompt from command arguments
        movie1_title = options['movie1']
        movie2_title = options['movie2']
        prompt = options['prompt']

        # Attempt to load OpenAI API key from .env files
        env_loaded_from_file = False
        env_file_paths = ['openAI.env', '../openAI.env', './openAI.env']
        for path in env_file_paths:
            if os.path.exists(path):
                load_dotenv(path)
                env_loaded_from_file = True
                self.stdout.write(f"Loaded environment variables from: {path}")
                break
        
        # Now, check if the API key is actually available in the environment
        api_key_value = os.environ.get('openai_apikey')
        
        if not api_key_value:
            error_msg = "OpenAI API key ('openai_apikey') not found. "
            if env_loaded_from_file:
                error_msg += "It was not found in the loaded .env file or as a platform environment variable."
            else:
                error_msg += "No .env file was found, and it was not set as a platform environment variable."
            self.stderr.write(self.style.ERROR(error_msg))
            return

        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key_value)
        
        # ✅ Function to get embeddings from OpenAI API
        def get_embedding(text):
            response = client.embeddings.create(input=[text], model="text-embedding-3-small")
            return np.array(response.data[0].embedding, dtype=np.float32)
        
        # ✅ Function to calculate cosine similarity between two vectors
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        try:
            # Try to find the movies in the database
            self.stdout.write(f"Looking for movies: '{movie1_title}' and '{movie2_title}'")
            
            try:
                movie1 = Movie.objects.get(title=movie1_title)
            except Movie.DoesNotExist:
                self.stdout.write(f"Movie '{movie1_title}' not found. Trying to find a similar movie...")
                movie1 = Movie.objects.filter(title__icontains=movie1_title).first()
                if not movie1:
                    self.stdout.write(f"No similar movie found for '{movie1_title}'. Using the first movie in the database.")
                    movie1 = Movie.objects.first()
                
            try:
                movie2 = Movie.objects.get(title=movie2_title)
            except Movie.DoesNotExist:
                self.stdout.write(f"Movie '{movie2_title}' not found. Trying to find a similar movie...")
                movie2 = Movie.objects.filter(title__icontains=movie2_title).first()
                if not movie2:
                    self.stdout.write(f"No similar movie found for '{movie2_title}'. Using the second movie in the database.")
                    movie2 = Movie.objects.exclude(id=movie1.id).first()
            
            # Print the selected movies
            self.stdout.write(f"Selected movies for comparison:")
            self.stdout.write(f"Movie 1: {movie1.title}")
            self.stdout.write(f"Movie 2: {movie2.title}")
            
            # ✅ Generate embeddings for both movies
            self.stdout.write("Generating embeddings for the movies...")
            emb1 = get_embedding(movie1.description)
            emb2 = get_embedding(movie2.description)
            
            # ✅ Calculate the similarity between the movies
            similarity = cosine_similarity(emb1, emb2)
            self.stdout.write(f"🎬 {movie1.title} vs {movie2.title}: {similarity:.4f}")
            
            # ✅ Calculate similarity with the prompt
            self.stdout.write(f"Comparing movies with prompt: '{prompt}'")
            
            # Get the embedding for the prompt
            prompt_emb = get_embedding(prompt)
            
            # Calculate similarities
            sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
            sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)
            
            # Display results
            self.stdout.write(f"📝 Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
            self.stdout.write(f"📝 Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")
            
            # Determine which movie is more similar to the prompt
            if sim_prompt_movie1 > sim_prompt_movie2:
                self.stdout.write(f"✅ '{movie1.title}' es más similar al prompt '{prompt}'")
            else:
                self.stdout.write(f"✅ '{movie2.title}' es más similar al prompt '{prompt}'")
                
        except Exception as e:
            self.stderr.write(f"Error calculating similarities: {str(e)}")
