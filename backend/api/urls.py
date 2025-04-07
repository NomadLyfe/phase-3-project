from django.urls import path, include
from . import views

urlpatterns = [
    path("profile/", views.ProfileCreateView.as_view(), name="profile"),
    path("creatematch/", views.ChessMatchCreateView.as_view(), name="create-match"),
    path("chessmatches/", views.ChessMatchListView.as_view(), name="chessmatch"),
    path(
        "chessmatch/<int:match_id>/forfeit/", views.forfeit_match, name="forfeit-match"
    ),
    path(
        "chessmatch/<int:pk>/",
        views.ChessMatchDetailView.as_view(),
        name="match-detail",
    ),
    path(
        "chessmatch/<int:match_id>/legal-moves/", views.legal_moves, name="legal-moves"
    ),
    path("chessmatch/<int:match_id>/move/", views.perform_move, name="perform-move"),
]
