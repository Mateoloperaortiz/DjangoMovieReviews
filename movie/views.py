from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Movie
import matplotlib
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def statistics_view(request):
    matplotlib.use('Agg')  # Backend para generar gráfica sin interfaz

    # OBTENER TODAS LAS PELÍCULAS
    all_movies = Movie.objects.all()

    # CONTAR PELÍCULAS POR AÑO
    movie_counts_by_year = {}

    for mv in all_movies:
        yr = mv.year if mv.year else "None"
        if yr in movie_counts_by_year:
            movie_counts_by_year[yr] += 1
        else:
            movie_counts_by_year[yr] = 1

    # GRÁFICA DE BARRAS - PELÍCULAS POR AÑO
    plt.figure(figsize=(10, 6))
    bar_positions = range(len(movie_counts_by_year))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # GUARDAR EN MEMORIA - GRÁFICA POR AÑO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # CONVERTIR A BASE64 - GRÁFICA POR AÑO
    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png)
    graphic_year = graphic_year.decode('utf-8')

    # CONTAR PELÍCULAS POR GÉNERO
    movie_counts_by_genre = {}

    for mv in all_movies:
        genre = mv.genre if mv.genre else "Unknown"
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    # GRÁFICA DE BARRAS - PELÍCULAS POR GÉNERO
    plt.figure(figsize=(12, 6))
    bar_positions = range(len(movie_counts_by_genre))
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=0.5, align='center', color='green')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=45)
    plt.subplots_adjust(bottom=0.3)

    # GUARDAR EN MEMORIA - GRÁFICA POR GÉNERO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # CONVERTIR A BASE64 - GRÁFICA POR GÉNERO
    image_png = buffer.getvalue()
    buffer.close()
    graphic_genre = base64.b64encode(image_png)
    graphic_genre = graphic_genre.decode('utf-8')

    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out successfully!")
    return redirect('home')