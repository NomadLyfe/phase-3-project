from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"chessmatch", views.ChessMatchViewSet, basename="chessmatch")

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("active-matches/", views.ActiveMatchList.as_view(), name="active-matches"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path(
        "chessmatch/<int:match_id>/computer-move/",
        views.computer_move,
        name="computer-move",
    ),
    path(
        "chessmatch/<int:match_id>/legal-moves/", views.legal_moves, name="legal-moves"
    ),
    path("", include(router.urls)),
]
