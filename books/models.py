from django.contrib.auth.models import User
from django.db import models

from books.api.utils import get_random_passcode


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passcode = models.IntegerField(default=get_random_passcode)
    created_date = models.DateTimeField()


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    description = models.TextField()


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorite_books')


class Rating(models.Model):
    book = models.ForeignKey('Book', related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"Rating: {self.rating} for {self.book.title}"
