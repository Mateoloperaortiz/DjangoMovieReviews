from django.shortcuts import render
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from movie.models import Movie
from .forms import RecommendationForm
import logging
from django.http import HttpResponse
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

# Set up logger
logger = logging.getLogger(__name__)

def get_embedding(client, text):
    """Get OpenAI embedding for a text"""
    try:
        response = client.embeddings.create(input=[text], model="text-embedding-3-small")
        return np.array(response.data[0].embedding, dtype=np.float32)
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        raise

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def test_recommend(request):
    """
    A simple test view to verify form submission works
    without relying on OpenAI API
    """
    recommended_movie = None
    error_message = None
    form = RecommendationForm()
    
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            # Instead of using OpenAI, just find a movie with the prompt in title or description
            movies = Movie.objects.filter(title__icontains=prompt) | Movie.objects.filter(description__icontains=prompt)
            
            if movies.exists():
                recommended_movie = movies.first()
                similarity_score = 0.95  # Dummy value
            else:
                error_message = f"No movies found matching: {prompt}"
    
    context = {
        'form': form,
        'recommended_movie': recommended_movie,
        'similarity_score': 0.95 if recommended_movie else None,
        'error_message': error_message,
    }
    
    return render(request, 'recommendations/recommend.html', context)

def recommend_movie(request):
    """
    View that recommends movies based on a similarity search with 
    the provided prompt - using precomputed embeddings for performance
    """
    recommended_movie = None
    similarity_score = None
    error_message = None
    
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        
        if prompt:
            # Try to find movies using OpenAI embeddings
            try:
                # Attempt to load OpenAI API key from .env files
                env_loaded_from_file = False
                for path in ['openAI.env', '../openAI.env', './openAI.env']:
                    if os.path.exists(path):
                        load_dotenv(path)
                        env_loaded_from_file = True
                        logger.info(f"Loaded environment variables from: {path}")
                        break
                
                api_key_value = os.environ.get('openai_apikey')

                if not api_key_value:
                    logger.warning("OpenAI API key ('openai_apikey') not found. Falling back to text search.")
                    # Fall back to text search if OpenAI is not available
                    movies = Movie.objects.filter(title__icontains=prompt) | Movie.objects.filter(description__icontains=prompt)
                    
                    if movies.exists():
                        recommended_movie = movies.first()
                        similarity_score = 0.75  # Approximate score
                    else:
                        error_message = f"No movies found matching: '{prompt}' (API key missing)."
                else:
                    # Use OpenAI embeddings
                    client = OpenAI(api_key=api_key_value)
                    
                    # Get embedding for the prompt
                    prompt_embedding = get_embedding(client, prompt)
                    
                    # Get movies with precomputed embeddings
                    movies_with_embeddings = Movie.objects.exclude(embedding__isnull=True)
                    
                    if not movies_with_embeddings.exists():
                        # No precomputed embeddings available, fall back to text search
                        movies = Movie.objects.filter(title__icontains=prompt) | Movie.objects.filter(description__icontains=prompt)
                        
                        if movies.exists():
                            recommended_movie = movies.first()
                            similarity_score = 0.7  # Approximate score
                            error_message = "Using text search (no embeddings available). Run 'python manage.py compute_embeddings' to improve results."
                        else:
                            error_message = f"No movies found matching: '{prompt}'"
                    else:
                        # Calculate similarity for each movie using precomputed embeddings
                        best_match = None
                        best_similarity = -1
                        
                        # Convert prompt embedding to list for comparison with stored JSON
                        prompt_embedding_list = prompt_embedding.tolist()
                        
                        for movie in movies_with_embeddings:
                            if not movie.embedding:
                                continue
                                
                            try:
                                # Convert stored embedding from JSON back to numpy array
                                movie_embedding = np.array(movie.embedding, dtype=np.float32)
                                similarity = cosine_similarity(prompt_embedding, movie_embedding)
                                
                                if similarity > best_similarity:
                                    best_similarity = similarity
                                    best_match = movie
                            except Exception as e:
                                logger.error(f"Error processing movie {movie.title}: {str(e)}")
                                continue
                        
                        if best_match:
                            recommended_movie = best_match
                            similarity_score = best_similarity
                        else:
                            # Try text search as fallback
                            movies = Movie.objects.filter(title__icontains=prompt) | Movie.objects.filter(description__icontains=prompt)
                            
                            if movies.exists():
                                recommended_movie = movies.first()
                                similarity_score = 0.7  # Approximate score
                            else:
                                error_message = f"No movies found matching: '{prompt}'"
            
            except Exception as e:
                error_message = f"Error retrieving recommendation: {str(e)}"
                logger.error(f"Error recommending movie: {str(e)}")
        else:
            error_message = "Please enter a search term."
    
    context = {
        'form': RecommendationForm(),
        'recommended_movie': recommended_movie,
        'similarity_score': similarity_score,
        'error_message': error_message,
    }
    
    return render(request, 'recommendations/recommend.html', context)

def direct_recommend(request, prompt):
    """
    Direct recommendation view that takes the prompt from the URL
    """
    recommended_movie = None
    similarity_score = None
    error_message = None
    
    # Use simple text search for now
    movies = Movie.objects.filter(title__icontains=prompt) | Movie.objects.filter(description__icontains=prompt)
    
    if movies.exists():
        recommended_movie = movies.first()
        similarity_score = 0.95  # Dummy value for testing
    else:
        error_message = f"No movies found matching: '{prompt}'"
    
    context = {
        'form': RecommendationForm(),
        'recommended_movie': recommended_movie,
        'similarity_score': similarity_score,
        'error_message': error_message,
        'prompt_used': prompt,
    }
    
    return render(request, 'recommendations/recommend.html', context)
