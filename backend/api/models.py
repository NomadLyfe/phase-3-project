from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    move_history = models.JSONField(default=list)
    board = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match #{self.id} - {self.player_white} vs {self.player_black or 'Computer'}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
