from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


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
    move_history = models.JSONField(default=list)  # list of {from, to, piece, ...}
    game_history = models.JSONField(default=list)  # list of serialized boards

    turn_color = models.CharField(max_length=5, default="white")
    turn_count = models.PositiveIntegerField(default=0)
    game_over = models.BooleanField(default=False)
    winner_color = models.CharField(
        max_length=5,
        choices=[("white", "White"), ("black", "Black"), ("draw", "Draw")],
        null=True,
        blank=True,
    )
    winner_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="won_matches",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_move_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    captured_by_white = models.JSONField(default=list)
    captured_by_black = models.JSONField(default=list)

    def __str__(self):
        return f"Match #{self.id} - {self.player_white} vs {self.player_black or 'Computer'}"

    def get_game(self):
        from .chess_objects import ChessGame

        game = ChessGame.deserialize_board(self.board)
        game.turn = self.turn_color
        return game

    def update_from_game(self, game):
        self.board = game.serialize_board()
        self.turn_color = game.turn
        self.turn_count += 1
        self.game_over = game.is_checkmate("white") or game.is_checkmate("black")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def all_matches(self):
        return ChessMatch.objects.filter(
            models.Q(player_white=self.user) | models.Q(player_black=self.user)
        )

    @property
    def active_matches(self):
        return self.all_matches.filter(game_over=False)

    @property
    def archived_matches(self):
        return self.all_matches.filter(game_over=True)

    @property
    def computed_wins(self):
        return self.all_matches.filter(game_over=True, winner_user=self.user).count()

    @property
    def computed_losses(self):
        return (
            self.all_matches.filter(game_over=True)
            .exclude(winner_user=self.user)
            .exclude(winner_color="draw")
            .count()
        )

    @property
    def computed_draws(self):
        return self.all_matches.filter(winner_color="draw").count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
