from django.db import models
from django.contrib.auth.models import User

from .models import Post  # if inside same file, this line is not needed; otherwise make sure Post is defined above

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # MUST be exactly this name

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

