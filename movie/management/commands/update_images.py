import os
import requests
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Generate movie poster images using OpenAI API and update the database"

    def handle(self, *args, **kwargs):
        # ✅ Load environment variables from the .env file
        # Try different possible locations for the .env file
        env_file_paths = ['openAI.env', '../openAI.env', './openAI.env']
        env_loaded = False
        
        for path in env_file_paths:
            if os.path.exists(path):
                load_dotenv(path)
                self.stdout.write(f"Loaded environment from: {path}")
                env_loaded = True
                break
        
        if not env_loaded:
            self.stderr.write(f"Could not find OpenAI env file in any of the expected locations.")
            return

        # Get API key from environment
        api_key = os.environ.get('openai_apikey')
        if not api_key:
            self.stderr.write(f"OpenAI API key not found in environment variables.")
            return

        # ✅ Initialize the OpenAI client with the API key
        client = OpenAI(
            api_key=api_key,
        )

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
            
            # ⚠️ Process only one movie to save API resources
            # 🚫 Don't remove this break as instructed
            break
            
        self.stdout.write(self.style.SUCCESS(f"Image generation and database update process completed."))

    def generate_and_download_image(self, client, movie_title, save_folder):
        """
        Generate an image using OpenAI API and download it to the specified folder
        """
        prompt = f"Movie poster of {movie_title}"
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            quality="standard",
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