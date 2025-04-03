from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


class ChessMatch(models.Model):
    player_white = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="white_matches",
        null=True,
        blank=True,
    )
    player_black = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="black_matches",
        null=True,
        blank=True,
    )
    board = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match #{self.id} - {self.player_white} vs {self.player_black or 'Computer'}"
