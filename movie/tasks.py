import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta
import logging
from .models import Movie

# Set up logger
logger = logging.getLogger(__name__)

def get_embedding(client, text):
    """Get OpenAI embedding for a text"""
    try:
        response = client.embeddings.create(input=[text], model="text-embedding-3-small")
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        raise

def update_movie_embeddings(max_per_run=10, force_update=False):
    """
    Update embeddings for movies that either:
    1. Have no embedding
    2. Have stale embeddings (older than 30 days)
    
    Args:
        max_per_run: Maximum number of movies to process in a single run
        force_update: If True, update all movies regardless of when they were last updated
    """
    logger.info(f"Starting movie embedding updates (max: {max_per_run}, force: {force_update})")
    
    # Load OpenAI API key
    env_loaded = False
    for path in ['openAI.env', '../openAI.env', './openAI.env']:
        if os.path.exists(path):
            load_dotenv(path)
            env_loaded = True
            logger.info(f"Loaded environment from: {path}")
            break
    
    if not env_loaded or not os.environ.get('openai_apikey'):
        logger.error('OpenAI API key not found')
        return
    
    client = OpenAI(api_key=os.environ.get('openai_apikey'))
    
    # Get movies that need updating
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    if force_update:
        # Update all movies
        movies_to_update = Movie.objects.all()
    else:
        # Update movies with no embedding or with stale embeddings
        movies_to_update = Movie.objects.filter(
            embedding__isnull=True
        ) | Movie.objects.filter(
            embedding_updated_at__lt=thirty_days_ago
        )
    
    # Limit the number of movies processed in a single run
    movies_to_update = movies_to_update[:max_per_run]
    
    logger.info(f"Found {movies_to_update.count()} movies to update")
    
    processed_count = 0
    for movie in movies_to_update:
        if not movie.description:
            logger.warning(f"Skipping {movie.title} - no description")
            continue
        
        try:
            # Get embedding for the movie description
            embedding = get_embedding(client, movie.description)
            
            # Store the embedding
            movie.embedding = embedding
            movie.embedding_updated_at = timezone.now()
            movie.save()
            
            processed_count += 1
            logger.info(f"Updated embedding for {movie.title}")
            
            # Add delay to avoid rate limiting
            import time
            time.sleep(0.5)
            
        except Exception as e:
            logger.error(f"Error processing movie {movie.title}: {str(e)}")
    
    logger.info(f"Completed embedding updates. Processed {processed_count} movies") 