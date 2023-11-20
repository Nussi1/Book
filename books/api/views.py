from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Author, Book, FavoriteBook, Genre, Rating, Review

from .serializers import (ActivationCodeSerializer, AuthorSerializer,
                          BookSerializer, FavoriteBookSerializer,
                          GenreSerializer, RatingSerializer, ReviewSerializer)


class ActivationCodeView(generics.GenericAPIView):
	serializer_class = ActivationCodeSerializer

	def post(self, request):
		passcode = request.data.get('passcode')

		activation_code = ActivationCode.objects.filter(
			passcode=passcode, created_date__gte=(dt.now() - timedelta(days=1))
		).first()

		print(activation_code, passcode, request.data)
		if activation_code is not None:
			user = activation_code.user
			if user.is_verified:
				return Response({'error': 'Already activated'}, status=status.HTTP_200_OK)
			user.is_verified = True
			user.save()
			return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
		return Response({'error': 'Invalid passcode'}, status=status.HTTP_400_BAD_REQUEST)


class BookListView(generics.ListCreateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = {
		'genre__name': ['exact'],
		'author__name': ['exact'],
		'publication_date': ['gte', 'lte']
	}


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer


class GenreListView(generics.ListCreateAPIView):
	queryset = Genre.objects.all()
	serializer_class = GenreSerializer


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Genre.objects.all()
	serializer_class = GenreSerializer


class AuthorListView(generics.ListCreateAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer


class ReviewCreateView(generics.CreateAPIView):
	queryset = Review.objects.all()
	serializer_class = ReviewSerializer


class RatingCreateView(generics.CreateAPIView):
	queryset = Rating.objects.all()
	serializer_class = RatingSerializer

	def perform_create(self, serializer):
		book_id = self.request.data.get('book')
		book = Book.objects.get(pk=book_id)
		serializer.save(book=book)


#
# class AddToFavoritesView(APIView):
# 	@swagger_auto_schema(request_body=openapi.Schema(
# 		type=openapi.TYPE_OBJECT,
# 		properties={
# 			'book_id': openapi.Schema(
# 				type=openapi.TYPE_INTEGER,
# 				description='ID of the book'
# 			)
# 		}
# 	))
# 	def post(self, request):
# 		user = request.user
# 		book_id = request.data.get('book_id')
#
# 		try:
# 			book = Book.objects.get(pk=book_id)
# 			FavoriteBook.objects.get_or_create(user=user, book=book)
# 			return Response({'message': 'Book added to favorites'}, status=status.HTTP_200_OK)
# 		except Book.DoesNotExist:
# 			return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
# 		except Exception as e:
# 			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class AddToFavoritesView(generics.CreateAPIView):
	serializer_class = FavoriteBookSerializer

	def create(self, request, *args, **kwargs):
		user = request.user
		book_id = request.data.get('book_id')

		try:
			book = Book.objects.get(pk=book_id)
			favorite_book, created = FavoriteBook.objects.get_or_create(user=user, book=book)
			if created:
				return Response({'message': 'Book added to favorites'}, status=status.HTTP_201_CREATED)
			else:
				return Response({'message': 'Book already in favorites'}, status=status.HTTP_200_OK)
		except Book.DoesNotExist:
			return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
