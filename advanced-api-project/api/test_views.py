from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):
    """Comprehensive tests for Book API endpoints"""

    def setUp(self):
        # Create a test user for authenticated endpoints
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.author = Author.objects.create(name="Author One")
        self.book1 = Book.objects.create(title="Book One", publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2021, author=self.author)

        # API endpoints
        self.list_url = reverse("book-list")
        self.detail_url = lambda pk: reverse("book-detail", args=[pk])
        self.create_url = reverse("book-create")
        self.update_url = lambda pk: reverse("book-update", args=[pk])
        self.delete_url = lambda pk: reverse("book-delete", args=[pk])

    # --------------------
    # TEST LIST VIEW
    # --------------------
    def test_list_books(self):
        """Anyone can list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    # --------------------
    # TEST DETAIL VIEW
    # --------------------
    def test_retrieve_book(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book One")

    # --------------------
    # TEST CREATE VIEW
    # --------------------
    def test_create_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------------------
    # TEST UPDATE VIEW
    # --------------------
    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        data = {"title": "Updated Title"}
        response = self.client.patch(self.update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_unauthenticated(self):
        data = {"title": "Updated Title"}
        response = self.client.patch(self.update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------------------
    # TEST DELETE VIEW
    # --------------------
    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --------------------
    # TEST FILTER, SEARCH, ORDER
    # --------------------
    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url, {"title": "Book One"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book One")

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {"search": "Book Two"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book Two")

    def test_order_books_by_publication_year(self):
        response = self.client.get(self.list_url, {"ordering": "publication_year"})
        self.assertEqual(response.data[0]["publication_year"], 2020)

