from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# Serializer for the Book model.
# It includes a custom validation to make sure
# publication_year is not in the future.
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation for publication_year
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value



# Serializer for Author model.
# This adds a nested list of books using the BookSerializer.
class AuthorSerializer(serializers.ModelSerializer):
    # nested serializer to show related books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

