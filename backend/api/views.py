from django.shortcuts import render
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    NoteSerializer,
    ChessMatchSerializer,
    ProfileSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, ChessMatch, Profile
from .bot import get_best_move

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

        if not (
            isinstance(from_pos, list)
            and isinstance(to_pos, list)
            and len(from_pos) == 2
            and len(to_pos) == 2
        ):
            return Response({"error": "Invalid position format."}, status=400)

        board = match.board
        from_rank, from_file = from_pos
        to_rank, to_file = to_pos

        piece = board[from_rank][from_file]
        if not piece:
            return Response({"error": "No piece at from position."}, status=400)

        # ✅ 1. Apply player move
        board[to_rank][to_file] = board[from_rank][from_file]
        board[from_rank][from_file] = None
        match.board = board
        match.move_history.append(
            {
                "player": request.user.username,
                "from": from_pos,
                "to": to_pos,
                "piece": piece,
            }
        )
        match.save()

        # ✅ 2. Determine if bot should move
        is_vs_computer = match.player_white is None or match.player_black is None
        current_player = request.user
        bot_move = None

        if is_vs_computer:
            from .bot import get_best_move

            if match.player_white == current_player:
                bot_color = "black"
            elif match.player_black == current_player:
                bot_color = "white"
            else:
                bot_color = None

            if bot_color:
                bot_move = get_best_move(match.board, bot_color)
                if bot_move:
                    fx, fy = bot_move[0]
                    tx, ty = bot_move[1]
                    match.board[tx][ty] = match.board[fx][fy]
                    match.board[fx][fy] = None
                    match.move_history.append(
                        {
                            "player": "Computer",
                            "from": [fx, fy],
                            "to": [tx, ty],
                            "piece": match.board[tx][ty],
                        }
                    )
                    match.save()

        return Response({"board": match.board, "bot_move": bot_move})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ActiveMatchList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        matches = ChessMatch.objects.filter(is_active=True).filter(
            models.Q(player_white=request.user) | models.Q(player_black=request.user)
        )
        data = [{"id": match.id} for match in matches]
        return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def computer_move(request, match_id):
    try:
        match = ChessMatch.objects.get(id=match_id, is_active=True)
    except ChessMatch.DoesNotExist:
        return Response({"error": "Match not found."}, status=404)

    board = match.board

    # determine bot color
    if match.player_white is None:
        bot_color = "white"
    elif match.player_black is None:
        bot_color = "black"
    else:
        return Response({"error": "Not a computer match."}, status=400)

    move = get_best_move(board, bot_color)
    if not move:
        match.is_active = False
        match.save()
        return Response({"message": "Game over", "board": board})

    # Apply move
    fx, fy = move[0]
    tx, ty = move[1]
    board[tx][ty] = board[fx][fy]
    board[fx][fy] = None
    match.board = board
    match.save()
    return Response({"board": board})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def legal_moves(request, match_id):
    match = get_object_or_404(ChessMatch, id=match_id)
    board = match.board
    from_square = request.data.get("from")  # expecting [x, y]

    if not from_square or len(from_square) != 2:
        return Response({"error": "Invalid from square"}, status=400)

    x, y = from_square
    piece = board[x][y]
    if not piece:
        return Response({"moves": []})

    color = "white" if piece.isupper() else "black"
    direction = -1 if color == "white" else 1
    moves = []

    def is_enemy(target):
        return target and (target.isupper() != piece.isupper())

    def add_move(nx, ny):
        if 0 <= nx < 8 and 0 <= ny < 8:
            target = board[nx][ny]
            if not target:
                moves.append({"from": [x, y], "to": [nx, ny], "type": "move"})
                return True
            elif is_enemy(target):
                moves.append({"from": [x, y], "to": [nx, ny], "type": "capture"})
        return False

    if piece.lower() == "p":  # Pawn
        start_row = 6 if piece.isupper() else 1
        one_step = x + direction
        two_step = x + 2 * direction

        if 0 <= one_step < 8 and board[one_step][y] is None:
            moves.append({"from": [x, y], "to": [one_step, y], "type": "move"})
            if x == start_row and board[two_step][y] is None:
                moves.append({"from": [x, y], "to": [two_step, y], "type": "move"})

        for dy in [-1, 1]:
            ny = y + dy
            nx = x + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if is_enemy(target):
                    moves.append({"from": [x, y], "to": [nx, ny], "type": "capture"})

    elif piece.lower() == "n":  # Knight
        knight_offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dx, dy in knight_offsets:
            nx, ny = x + dx, y + dy
            add_move(nx, ny)

    elif piece.lower() in ["b", "r", "q"]:
        directions = []
        if piece.lower() in ["b", "q"]:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.lower() in ["r", "q"]:
            directions += [(0, -1), (-1, 0), (0, 1), (1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if not add_move(nx, ny):
                    break
                nx += dx
                ny += dy

    elif piece.lower() == "k":  # King
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    nx, ny = x + dx, y + dy
                    add_move(nx, ny)

    return Response({"moves": moves})
