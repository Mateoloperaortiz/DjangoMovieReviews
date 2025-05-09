import os
import requests
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate movie poster images using OpenAI API and update the database"

    def handle(self, *args, **kwargs):
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

        # Create the images folder if it doesn't exist
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        # Get all movies from the database
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        # Process each movie
        for movie in movies:
            self.stdout.write(f"Processing movie: {movie.title}")
            
            # Generate and download the image, then update the movie
            image_relative_path = self.generate_and_download_image(client, movie.title, images_folder)
            
            # Update the movie with the new image path
            movie.image = image_relative_path
            movie.save()
            
            self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))
            
            # The break statement below was removed to allow processing multiple images.
            # Consider API rate limits and costs if processing a large number of images.
            # break 
            
        self.stdout.write(self.style.SUCCESS(f"Image generation and database update process completed for all iterated movies."))

    def generate_and_download_image(self, client, movie_title, save_folder):
        """
        Generate an image using OpenAI API and download it to the specified folder
        """
        prompt = f"Movie poster of {movie_title}"
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            # quality="standard", # Removed: 'quality' parameter is not supported by dall-e-2
            n=1,
        )
        image_url = response.data[0].url

        image_filename = f"m_{movie_title}.png"
        image_path_full = os.path.join(save_folder, image_filename)

        image_response = requests.get(image_url)
        image_response.raise_for_status()
        with open(image_path_full, 'wb') as f:
            f.write(image_response.content)

        return os.path.join('movie/images', image_filename)
