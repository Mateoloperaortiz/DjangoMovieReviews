import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from the images folder"

    def handle(self, *args, **kwargs):
        # Path to the folder with the images
        images_folder = 'media/movie/images/'
        
        # Check if the folder exists
        if not os.path.exists(images_folder):
            self.stderr.write(f"Images folder '{images_folder}' not found.")
            return
        
        # Get all movie images in the folder
        image_files = [f for f in os.listdir(images_folder) if f.startswith('m_') and f.endswith('.png')]
        self.stdout.write(f"Found {len(image_files)} images in the folder")
        
        # Get all movies from the database
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")
        
        # Create a dictionary to store image filenames by movie title
        image_map = {}
        for image_file in image_files:
            # Extract movie title from filename (remove 'm_' prefix and '.png' suffix)
            movie_title = image_file[2:-4]  # Remove 'm_' and '.png'
            image_map[movie_title] = image_file
        
        updated_count = 0
        not_found_count = 0
        
        # Update each movie with its corresponding image
        for movie in movies:
            # Try to find an exact match first
            image_file = None
            if movie.title in image_map:
                image_file = image_map[movie.title]
            else:
                # Try to find a close match
                for title in image_map:
                    if movie.title.lower() in title.lower() or title.lower() in movie.title.lower():
                        image_file = image_map[title]
                        break
            
            if image_file:
                # Update movie with image path
                image_path = os.path.join('movie/images', image_file)
                movie.image = image_path
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                not_found_count += 1
                self.stdout.write(self.style.WARNING(f"No matching image found for: {movie.title}"))
        
        # Print summary
        self.stdout.write(self.style.SUCCESS(f"✅ Updated images for {updated_count} movies"))
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(f"⚠️ Could not find images for {not_found_count} movies")) 