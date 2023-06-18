from django.db.models import Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer
from .models import Movie, Director, Review


@api_view(['GET'])
def movie_reviews_api_view(request):
    movies = Movie.objects.all()
    data = []
    for movie in movies:
        reviews = Review.objects.filter(movie=movie)
        avg_rating = reviews.aggregate(Avg('stars'))['stars__avg']
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'duration': movie.duration,
            'reviews': [
                {
                    'id': review.id,
                    'text': review.text,
                    'stars': review.stars
                }
                for review in reviews
            ],
            'avg_rating': avg_rating
        }
        data.append(movie_data)
    return Response(data=data)


@api_view(['GET'])
def director_list_api_view(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(directors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def director_item_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'Director not found!'}, status=status.HTTP_404_NOT_FOUND)
    serializer = DirectorSerializer(director)
    return Response(serializer.data)


@api_view(['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_item_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def review_item_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'Review not found!'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)
