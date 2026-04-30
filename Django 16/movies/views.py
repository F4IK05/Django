from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from movies.forms import MovieForm
from movies.models import Movie, Genre


# Create your views here.
@login_required
def movie_list(request):
    movies = Movie.objects.all().filter(owner=request.user)

    status = request.GET.get('status')
    genre = request.GET.get('genre')

    if status:
        movies = movies.filter(status=status)
    if genre:
        movies = movies.filter(genre=genre)

    genres = Genre.objects.all()

    return render(request, 'movies/movie_watchlist.html', {'movies': movies, 'genres': genres})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = request.user
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()

    return render(request, 'movies/add_to_watchlist.html', {'form': form})

@login_required
def edit_movie(request):
    movie = get_object_or_404(Movie, id=id, owner=request.user)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movies/edit_movie_detail.html', {'form': form})

@login_required
def delete_movie(request):
    movie = get_object_or_404(Movie, id=id, owner=request.user)

    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')

    return render(request, 'movies/delete_from_watchlist.html', {'movie': movie})