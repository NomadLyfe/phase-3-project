from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import generics, viewsets, status
from .serializers import UserSerializer, NoteSerializer, ChessMatchSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, ChessMatch

# Create your views here.


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            serializer.save(author=user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ChessMatchViewSet(viewsets.ModelViewSet):
    queryset = ChessMatch.objects.all()
    serializer_class = ChessMatchSerializer

    def perform_create(self, serializer):
        data = self.request.data
        user = self.request.user
        vs_computer = data.get("vs_computer", False)
        color = data.get("player_color", "white")

        if vs_computer:
            if color == "white":
                serializer.save(
                    player_white=user, player_black=None, board=self._starting_board()
                )
            else:
                serializer.save(
                    player_white=None, player_black=user, board=self._starting_board()
                )
        else:
            # multiplayer mode fallback
            serializer.save(player_white=user, board=self._starting_board())

    def _starting_board(self):
        layout = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p"] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ["P"] * 8,
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]
        return layout

    def _is_valid_position(self, pos):
        return len(pos) == 2 and pos[0] in "abcdefgh" and pos[1] in "12345678"

    def _pos_to_coords(self, pos):
        file = ord(pos[0]) - ord("a")
        rank = 8 - int(pos[1])
        return rank, file

    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        match = self.get_object()
        from_pos = request.data.get("from")
        to_pos = request.data.get("to")

        if not (from_pos and to_pos):
            return Response({"error": "Missing 'from' or 'to' position."}, status=400)

        if not (self._is_valid_position(from_pos) and self._is_valid_position(to_pos)):
            return Response({"error": "Invalid position format."}, status=400)

        board = match.board
        from_rank, from_file = self._pos_to_coords(from_pos)
        to_rank, to_file = self._pos_to_coords(to_pos)

        piece = board[from_rank][from_file]
        if not piece:
            return Response({"error": "No piece at from position."}, status=400)

        # Basic placeholder movement logic
        board[to_rank][to_file] = piece
        board[from_rank][from_file] = None
        match.board = board
        match.save()

        return Response({"board": board}, status=200)
