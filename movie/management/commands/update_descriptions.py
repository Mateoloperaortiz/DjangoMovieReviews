from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

class Command(BaseCommand):
    help = 'Update missing movie descriptions using the OpenAI API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all movie descriptions, not just empty ones',
        )

    def handle(self, *args, **options):
        # Look for the .env file in various possible locations
        env_paths = [
            'openAI.env',                      # Project root
            os.path.join(os.getcwd(), 'openAI.env'), # Absolute path to root
            '../openAI.env',                   # One level up
            '../../openAI.env',                # Two levels up
        ]
        
        env_loaded = False
        env_path_used = None
        
        for env_path in env_paths:
            if os.path.exists(env_path):
                self.stdout.write(f"Loading environment variables from: {env_path}")
                load_dotenv(env_path)
                env_loaded = True
                env_path_used = env_path
                break
                
        if not env_loaded:
            self.stdout.write(self.style.ERROR("Could not find openAI.env file. Searched in: " + ", ".join(env_paths)))
            return
            
        # Verify that the API key is available
        api_key = os.environ.get('openai_apikey')
        if not api_key:
            self.stdout.write(self.style.ERROR(f"API key 'openai_apikey' not found in {env_path_used}"))
            return
            
        self.stdout.write(f"API key found: {api_key[:5]}...{api_key[-5:]}")
            
        try:
            # Initialize the OpenAI client with the API Key
            client = OpenAI(api_key=api_key)

            # Define the general instruction for description generation
            instruction = """
            Act as an expert film critic. Your task is to create a movie description for a database of movie reviews.
            The description should be informative yet concise, with a professional and engaging style, including:
            - A brief synopsis of the plot without revealing major twists
            - The main genre
            - Mention of notable actors or director, if relevant
            - A touch of context about its importance in film history, if applicable
            
            The description should be 2-4 sentences and objective.
            """

            # Helper function to get the API response
            def get_completion(prompt, model="gpt-3.5-turbo"):
                # Define the message with the 'user' role and the content we send
                messages = [{"role": "user", "content": prompt}]
                
                # Call the API with the model and messages
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7  # Controls creativity
                )
                
                # Return only the content of the generated response
                return response.choices[0].message.content.strip()

            # Get movies with empty descriptions or all movies if --all flag is used
            if options['all']:
                movies = Movie.objects.all()
                self.stdout.write(f"Processing all {movies.count()} movies in the database.")
            else:
                movies = Movie.objects.filter(description='')
                self.stdout.write(f"Found {movies.count()} movies with empty descriptions.")
            
            if not movies:
                self.stdout.write(self.style.WARNING("No movies to process."))
                return
                
            count = 0
            
            for movie in movies:
                try:
                    # Create context-rich prompt
                    context = f"Title: {movie.title}"
                    if movie.year:
                        context += f", Year: {movie.year}"
                    if movie.genre:
                        context += f", Genre: {movie.genre}"
                    
                    prompt = f"{instruction}\n\nCreate a description for this movie:\n{context}"
                    self.stdout.write(f"Processing movie: {movie.title}")
                    
                    response = get_completion(prompt)
                    
                    movie.description = response
                    movie.save()
                    
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Description updated for: {movie.title}"))
                    self.stdout.write(f"New description: {response}")
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error updating movie {movie.title}: {str(e)}"))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} movie descriptions.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"General error: {str(e)}")) 