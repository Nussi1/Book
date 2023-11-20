from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (AddToFavoritesView, AuthorDetailView, AuthorListView,
                    BookDetailView, BookListView, GenreDetailView,
                    GenreListView, RatingCreateView, ReviewCreateView)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('author/', AuthorListView.as_view(), name='author-list'),
    path('author/<int:pk>', AuthorDetailView.as_view(), name='author-detail'),

    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>', GenreDetailView.as_view(), name='genre-detail'),

    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    path('create-review/', ReviewCreateView.as_view(), name='create-review'),
    path('create-rating/', RatingCreateView.as_view(), name='create-rating'),
    path('add_to_favorites/', AddToFavoritesView.as_view(), name='add_to_favorites'),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
