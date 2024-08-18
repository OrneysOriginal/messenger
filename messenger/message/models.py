from django.db import models
from django.core.validators import validate_slug


class Author(models.Model):
    username = models.CharField(max_length=255, validators=[validate_slug])


class Messages(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='author',
        related_query_name='author',
    )
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
