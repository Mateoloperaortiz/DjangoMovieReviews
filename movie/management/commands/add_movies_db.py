from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = 'Load movies from movies.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        json_file_path = 'movie/management/commands/movies.json'
        
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        # Add movies to the database
        count = 0
        for i in range(min(100, len(movies))):
            movie = movies[i]
            exist = Movie.objects.filter(title=movie['title']).first()  # Check if the movie already exists
            
            # Get plot/description with a default value if missing
            plot = movie.get('plot', '')
            if plot is None:  # Handle None values
                plot = ''
                
            if not exist:              
                try:
                    Movie.objects.create(
                        title=movie['title'],
                        image='movie/images/default.jpg',
                        genre=movie.get('genre', ''),  # Use get with default for optional fields
                        year=movie.get('year'),
                        description=plot,
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding movie {movie["title"]}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} movies.')) 