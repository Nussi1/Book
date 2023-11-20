from django.db.models import Avg
from rest_framework import serializers

from books.models import Author, Book, FavoriteBook, Genre, Rating, Review


class ActivationCodeSerializer(serializers.Serializer):
    passcode = serializers.IntegerField()

    class Meta:
        fields = ['passcode']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_average_rating(self, obj):
        ratings = Rating.objects.filter(book=obj)
        if ratings.exists():
            average = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
            return average
        return None

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorite_books.filter(user=request.user).exists()
        return False
