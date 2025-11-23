from django.urls import path
from . import views

urlpatterns = [
    # Function-based view: list all books
    path('books/', views.list_books, name='list_books'),

    # Class-based view: library detail
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
]
