from django.db import models

# Author model stores the name of the author.
# One Author can have many Books.
class Author(models.Model):
    name = models.CharField(max_length=100)  # simple name field

    def __str__(self):
        return self.name


# Book model stores info about each book.
# It is connected to Author using a ForeignKey,
# which creates a one-to-many relationship (one author → many books).
class Book(models.Model):
    title = models.CharField(max_length=200)  # book title
    publication_year = models.IntegerField()  # year published

    # foreign key connects each book to an author
    author = models.ForeignKey(
        Author,
        related_name="books",      # allows Author.books to access all their books
        on_delete=models.CASCADE   # delete books if author is deleted
    )

    def __str__(self):
        return self.title
