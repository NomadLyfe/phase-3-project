from copy import deepcopy
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from .models import ChessMatch
from .serializers import (
    UserSerializer,
    ChessMatchSerializer,
    ProfileSerializer,
)
from .chess_objects import ChessGame
from .bot import get_best_move


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class ActiveMatchList(generics.ListAPIView):
    serializer_class = ChessMatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChessMatch.objects.filter(is_active=True).filter(
            models.Q(player_white=self.request.user)
            | models.Q(player_black=self.request.user)
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def legal_moves(request, match_id):
    match = get_object_or_404(ChessMatch, id=match_id)
    from_square = request.data.get("from")
    if not from_square or len(from_square) != 2:
        return Response({"error": "Invalid 'from' position."}, status=400)

    game = ChessGame.deserialize_board(match.board)
    game.turn = match.turn_color

    piece = game.get_piece(tuple(from_square))
    if not piece or piece.color != game.turn:
        return Response({"moves": []})

    legal_moves = []
    for to_pos in piece.possible_moves(game):
        game_copy = ChessGame.deserialize_board(game.serialize_board())
        game_copy.turn = game.turn
        game_copy.move_piece(piece.pos, to_pos)
        if game_copy.in_check(game.turn):
            continue
        move_type = "move"
        if game.get_piece(to_pos):
            move_type = "capture"
        if game_copy.in_check("black" if game.turn == "white" else "white"):
            move_type = "check"
            if game_copy.is_checkmate("black" if game.turn == "white" else "white"):
                move_type = "checkmate"
        legal_moves.append({"to": list(to_pos), "type": move_type})

    return Response({"moves": legal_moves})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def perform_move(request, match_id):
    match = get_object_or_404(ChessMatch, id=match_id)
    from_pos = request.data.get("from")
    to_pos = request.data.get("to")
    if not from_pos or not to_pos:
        return Response({"error": "Missing positions."}, status=400)

    game = ChessGame.deserialize_board(deepcopy(match.board))
    game.turn = match.turn_color

    if not game.move_piece(tuple(from_pos), tuple(to_pos)):
        return Response({"error": "Illegal move."}, status=400)

    match.board = deepcopy(game.serialize_board())
    match.turn_color = game.turn
    match.turn_count += 1
    match.move_history.append({"from": from_pos, "to": to_pos})
    match.game_history.append(deepcopy(match.board))

    in_check = game.in_check(game.turn)
    game_over = game.is_checkmate(game.turn)
    match.game_over = game_over

    if game_over:
        match.winner_color = "black" if game.turn == "white" else "white"
        match.winner_user = (
            match.player_white if match.winner_color == "white" else match.player_black
        )

    match.save()
    response = {
        "board": match.board,
        "move": {"from": from_pos, "to": to_pos},
        "in_check": in_check,
        "game_over": game_over,
    }

    if (match.player_white is None or match.player_black is None) and not game_over:
        bot_color = "black" if match.player_white == request.user else "white"
        game = ChessGame.deserialize_board(deepcopy(match.board))
        game.turn = bot_color
        bot_move = get_best_move(game, bot_color)
        print("BOT MOVE:", bot_move)
        if bot_move and isinstance(bot_move, (list, tuple)) and len(bot_move) == 2:
            print("[AI] Trying move_piece on:", bot_move)
            print("[AI] Piece at from_pos:", game.get_piece(bot_move[0]))
            print("[AI] Game turn:", game.turn)
            if game.move_piece(*bot_move):
                match.board = deepcopy(game.serialize_board())
                match.turn_color = game.turn
                match.turn_count += 1
                match.move_history.append(
                    {"from": list(bot_move[0]), "to": list(bot_move[1])}
                )
                match.game_history.append(deepcopy(match.board))

                if game.is_checkmate(game.turn):
                    match.game_over = True
                    match.winner_color = bot_color
                    match.winner_user = None

                print(f"[AI] Applying move {bot_move} and saving match {match.id}")
                match.save()
                response["bot_move"] = {
                    "from": list(bot_move[0]),
                    "to": list(bot_move[1]),
                }
                response["board"] = match.board
                response["game_over"] = match.game_over

    return Response(response)


class ChessMatchCreateView(generics.CreateAPIView):
    queryset = ChessMatch.objects.all()
    serializer_class = ChessMatchSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        player_color = self.request.data.get("player_color", "white")
        vs_computer = self.request.data.get("vs_computer", False)

        game = ChessGame()
        game.setup_board()

        if vs_computer:
            if player_color == "white":
                serializer.save(
                    player_white=self.request.user,
                    player_black=None,
                    board=deepcopy(game.serialize_board()),
                    turn_color="white",
                )
            else:
                game.turn = "white"
                move = get_best_move(game, "white")
                if move:
                    game.move_piece(*move)

                board_copy = deepcopy(game.serialize_board())
                serializer.save(
                    player_white=None,
                    player_black=self.request.user,
                    board=board_copy,
                    move_history=(
                        [{"from": list(move[0]), "to": list(move[1])}] if move else []
                    ),
                    game_history=[deepcopy(board_copy)],
                    turn_color=game.turn,
                )
        else:
            serializer.save(
                player_white=self.request.user,
                board=deepcopy(game.serialize_board()),
                turn_color="white",
            )


class ChessMatchListView(generics.ListAPIView):
    serializer_class = ChessMatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChessMatch.objects.filter(
            models.Q(player_white=self.request.user)
            | models.Q(player_black=self.request.user)
        )


class ChessMatchDetailView(generics.RetrieveAPIView):
    queryset = ChessMatch.objects.all()
    serializer_class = ChessMatchSerializer
    permission_classes = [IsAuthenticated]
