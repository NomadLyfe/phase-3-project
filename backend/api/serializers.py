from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, ChessMatch, Profile

# from .models import Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


class ChessMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessMatch
        fields = ["id", "player_white", "player_black", "board", "created_at"]
        read_only_fields = ["created_at", "player_white"]
        extra_kwargs = {"player_black": {"allow_null": True, "required": False}}


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = ["username", "avatar", "wins", "losses"]
