from django.urls import path, include
from . import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("creatematch/", views.ChessMatchCreateView.as_view(), name="create-match"),
    path(
        "chessmatch/<int:pk>/",
        views.ChessMatchDetailView.as_view(),
        name="match-detail",
    ),
    path("active-matches/", views.ActiveMatchList.as_view(), name="active-matches"),
    path(
        "chessmatch/<int:match_id>/legal-moves/", views.legal_moves, name="legal-moves"
    ),
    path("chessmatch/<int:match_id>/move/", views.perform_move, name="perform-move"),
]
