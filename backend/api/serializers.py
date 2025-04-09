from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ChessMatch, Profile

# from .models import Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChessMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessMatch
        fields = [
            "id",
            "player_white",
            "player_black",
            "board",
            "turn_color",
            "turn_count",
            "game_over",
            "winner_color",
            "winner_user",
            "move_history",
            "game_history",
            "created_at",
            "last_move_at",
            "ended_at",
        ]
        read_only_fields = ["created_at", "last_move_at", "player_white", "winner_user"]
        extra_kwargs = {"player_black": {"allow_null": True, "required": False}}


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    wins = serializers.SerializerMethodField()
    losses = serializers.SerializerMethodField()
    draws = serializers.SerializerMethodField()
    active_games = serializers.SerializerMethodField()
    archived_games = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "username",
            "avatar",
            "wins",
            "losses",
            "draws",
            "active_games",
            "archived_games",
        ]

    def get_wins(self, obj):
        return obj.computed_wins

    def get_losses(self, obj):
        return obj.computed_losses

    def get_draws(self, obj):
        return obj.computed_draws

    def get_active_games(self, obj):
        return obj.active_matches.count()

    def get_archived_games(self, obj):
        return obj.archived_matches.count()
