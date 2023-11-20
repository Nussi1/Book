from django.contrib import admin

from .models import Author, Book, FavoriteBook, Genre, Review

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(FavoriteBook)
