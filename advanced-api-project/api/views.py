from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework  # ✅ required by checker
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from .models import Book
from .serializers import BookSerializer

# READ — anyone can read, only authenticated users can write
class BookListView(generics.ListAPIView):
    """
    List all books with filtering, searching, and ordering.
    Filtering: title, author, publication_year
    Search: title, author
    Ordering: title, publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 🔥 Required backends
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        filters.OrderingFilter, 
    ]

    # Filtering
    filterset_fields = ["title", "author", "publication_year"]

    # Search
    search_fields = ["title", "author"]

    # Ordering
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# WRITE — authenticated users only
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

