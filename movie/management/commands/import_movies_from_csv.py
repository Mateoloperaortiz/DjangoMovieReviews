import os
import csv
from django.core.management.base import BaseCommand
from movie.models import Movie
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = "Import movies from a CSV file to the database"
    
    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, default='movies_initial.csv', 
                            help='Path to the CSV file containing movie data')
        parser.add_argument('--limit', type=int, default=100, 
                            help='Maximum number of movies to import')
        parser.add_argument('--offset', type=int, default=0, 
                            help='Number of rows to skip in the CSV (excluding header)')
        
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        limit = options['limit']
        offset = options['offset']
        
        if not os.path.exists(csv_file_path):
            self.stderr.write(f"CSV file not found at {csv_file_path}")
            return
        
        self.stdout.write(f"Importing movies from {csv_file_path} (offset: {offset}, limit: {limit})...")
        
        # Keep track of successful and failed imports
        success_count = 0
        skip_count = 0
        error_count = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Skip rows according to offset
            for i in range(offset):
                try:
                    next(reader)
                except StopIteration:
                    self.stderr.write(f"Offset {offset} is greater than the number of rows in the CSV")
                    return
            
            # Process rows up to the limit
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                
                title = row.get('title', '').strip()
                
                # Skip if no title
                if not title:
                    self.stdout.write(f"Skipping row {offset+i+1}: No title found")
                    skip_count += 1
                    continue
                
                # Check if movie already exists
                if Movie.objects.filter(title=title).exists():
                    self.stdout.write(f"Skipping '{title}': Already in database")
                    skip_count += 1
                    continue
                
                try:
                    # Extract movie data
                    year = int(row.get('year', 0)) if row.get('year', '').isdigit() else None
                    genre = row.get('genre', '')
                    
                    # Get plot as description
                    description = row.get('plot', '') or row.get('fullplot', '')
                    if not description:
                        description = f"A {genre.lower()} movie released in {year}." if genre and year else "No description available."
                    
                    # Create movie object
                    movie = Movie(
                        title=title,
                        description=description,
                        genre=genre,
                        year=year
                    )
                    
                    # Try to get poster image if URL is available
                    poster_url = row.get('poster', '')
                    if poster_url and poster_url.startswith('http'):
                        try:
                            response = requests.get(poster_url, timeout=5)
                            if response.status_code == 200:
                                image_name = f"{title.replace(' ', '_')}.jpg"
                                movie.image.save(image_name, ContentFile(response.content), save=False)
                        except Exception as e:
                            self.stdout.write(f"Could not download image for '{title}': {str(e)}")
                    
                    # Save the movie
                    movie.save()
                    success_count += 1
                    
                    self.stdout.write(f"Added '{title}' ({year}) to database")
                    
                except Exception as e:
                    self.stderr.write(f"Error importing '{title}': {str(e)}")
                    error_count += 1
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f"Import completed: {success_count} added, {skip_count} skipped, {error_count} errors")) 