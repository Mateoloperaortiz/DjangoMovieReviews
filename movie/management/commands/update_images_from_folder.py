import os
import re
from django.core.management.base import BaseCommand
from movie.models import Movie

def normalize_title_for_matching(title_str):
    # Lowercase
    s = title_str.lower()
    # Replace specific problematic characters with space
    s = re.sub(r'[:&?]', ' ', s)
    # Remove other characters that are not alphanumeric, space, or hyphen
    s = re.sub(r'[^\w\s-]', '', s)
    # Collapse multiple spaces/hyphens into a single space and strip
    s = re.sub(r'[\s-]+', ' ', s).strip()
    return s

class Command(BaseCommand):
    help = "Update movie images from the images folder"

    def handle(self, *args, **kwargs):
        images_folder = 'images/'
        
        if not os.path.exists(images_folder):
            self.stderr.write(f"Images folder '{images_folder}' not found.")
            return
        
        image_files = [f for f in os.listdir(images_folder) if f.startswith('m_') and f.endswith('.png')]
        self.stdout.write(f"Found {len(image_files)} images in the folder")
        
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies in the database")
        
        image_map = {}
        for image_file in image_files:
            raw_title_from_filename = image_file[2:-4]  # Remove 'm_' and '.png'
            normalized_filename_key = normalize_title_for_matching(raw_title_from_filename)
            if normalized_filename_key: # Avoid empty keys if filename was all special chars
                image_map[normalized_filename_key] = image_file
        
        updated_count = 0
        not_found_count = 0
        
        for movie in movies:
            image_file = None
            normalized_db_title = normalize_title_for_matching(movie.title)

            if not normalized_db_title: # Should not happen if movie titles are reasonable
                self.stdout.write(self.style.WARNING(f"Could not normalize DB title: {movie.title}"))
                not_found_count += 1
                continue

            # Try to find an exact match on normalized titles
            if normalized_db_title in image_map:
                image_file = image_map[normalized_db_title]
            else:
                # Fallback to substring matching on normalized titles
                for map_key_normalized, original_filename in image_map.items():
                    if map_key_normalized in normalized_db_title:
                        image_file = original_filename
                        self.stdout.write(f"Partial match (image key in DB title): DB '{movie.title}' (norm: '{normalized_db_title}') with ImgKey '{map_key_normalized}' (file: '{original_filename}')")
                        break
                    elif normalized_db_title in map_key_normalized:
                        image_file = original_filename
                        self.stdout.write(f"Partial match (DB title in image key): DB '{movie.title}' (norm: '{normalized_db_title}') with ImgKey '{map_key_normalized}' (file: '{original_filename}')")
                        break
            
            if image_file:
                image_path = os.path.join('images', image_file)
                movie.image = image_path
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                not_found_count += 1
                self.stdout.write(self.style.WARNING(f"No matching image found for: {movie.title} (Normalized DB title: '{normalized_db_title}')"))

        self.stdout.write(self.style.SUCCESS(f"✅ Updated images for {updated_count} movies"))
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(f"⚠️ Could not find images for {not_found_count} movies"))
