import os
import csv
from django.core.management.base import BaseCommand
from movie.models import Movie
from django.db.models import Q

class Command(BaseCommand):
    help = "Update movie descriptions in the database from a CSV file"

    def handle(self, *args, **kwargs):
        # 📥 Ruta del archivo CSV con las descripciones actualizadas
        csv_file = 'updated_movie_descriptions.csv'  # ← Puedes cambiar el nombre si es necesario

        # ✅ Verifica si el archivo existe
        if not os.path.exists(csv_file):
            self.stderr.write(f"CSV file '{csv_file}' not found.")
            return

        updated_count = 0

        # 📖 Primero contamos cuántas películas hay en el CSV
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            total_count = len(rows)
            self.stdout.write(f"Found {total_count} movies in CSV")

        # 📖 Abrimos el CSV nuevamente para procesar las actualizaciones
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row['Title']
                new_description = row['Updated Description']
                
                self.stdout.write(f"Processing: {title}")

                try:
                    # Intentar buscar la película con coincidencia exacta (case-insensitive)
                    movie = Movie.objects.filter(title__iexact=title).first()
                    
                    # Si no se encuentra, intentar con coincidencia parcial
                    if not movie:
                        self.stdout.write(f"Exact match not found, trying partial match for: {title}")
                        movie = Movie.objects.filter(title__icontains=title).first()
                        
                        # Si sigue sin encontrarse, intentar una búsqueda más agresiva
                        if not movie:
                            # Extraer palabras clave del título (ignorando artículos)
                            keywords = [word for word in title.lower().split() if word not in ['the', 'a', 'an']]
                            if keywords:
                                query = Q()
                                for keyword in keywords:
                                    if len(keyword) > 3:  # Ignorar palabras muy cortas
                                        query |= Q(title__icontains=keyword)
                                
                                movie = Movie.objects.filter(query).first()
                    
                    if not movie:
                        raise Movie.DoesNotExist()
                        
                    # Mostrar qué película se encontró (por si la coincidencia no es exacta)
                    self.stdout.write(f"Found movie in database: {movie.title}")

                    # Actualizar la descripción de la película
                    movie.description = new_description
                    movie.save()
                    updated_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))

                except Movie.DoesNotExist:
                    self.stderr.write(f"Movie not found: {title}")
                except Exception as e:
                    self.stderr.write(f"Failed to update {title}: {str(e)}")

        # ✅ Al finalizar, muestra cuántas películas se actualizaron
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies from CSV.")) 