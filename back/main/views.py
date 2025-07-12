from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum, Count, F, Value, IntegerField
from django.utils import timezone
from rest_framework.views import APIView

from .models import *
from .serializers import *


class RegisterView(generics.CreateAPIView):
    """
    POST /api/register/
    {
        "username": "...",
        "email": "...",
        "password": "...",
        "password2": "..."
    }
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    """
    POST /api/logout/
    {
        "refresh": "<refresh_token>"
    }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh = RefreshToken(request.data["refresh"])
            refresh.blacklist()          # adds it to the blacklist table
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):
    """
    POST /api/change-password/
    {
        "current_password": "...",
        "new_password": "..."
    }
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # we only ever change the password for the current user
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"detail": "Password changed"}, status=status.HTTP_200_OK)


class DeleteAccountView(generics.DestroyAPIView):
    """
    DELETE /api/delete-account/
    """
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user.delete()                  # physically deletes; use `is_active=False` if you prefer
        return Response(status=status.HTTP_204_NO_CONTENT)


class VimoSessionCreateView(generics.CreateAPIView):
    """
    POST  /api/vimo/           → create **one** session row

    body ▸  {
               "focus_time": 1500,
               "break_time": 300,
               "session":    1,
               "balance":    10
             }
    """
    serializer_class    = VimoSerializer
    permission_classes  = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VimoAllStatsView(APIView):
    """
    GET  /api/vimo/            → lifetime totals for the logged-in user

    response ▸ {
                 "focus_time":  72_000,
                 "break_time":  9_000,
                 "all_time":    81_000,
                 "sessions":    40,
                 "balance":     280
               }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        totals = (
            Vimo.objects
                .filter(user=request.user)
                .aggregate(
                    focus_time = Sum("focus_time"),
                    break_time = Sum("break_time"),
                    sessions   = Sum("session"),
                    balance    = Sum("balance"),
                )
        )

        # Replace None with 0 and compute all_time
        totals = {k: totals.get(k) or 0 for k in totals}
        totals["all_time"] = totals["focus_time"] + totals["break_time"]
        return Response(totals, status=status.HTTP_200_OK)


class VimoTodayStatsView(APIView):
    """
    GET  /api/vimo/today/      → today's focus & session count only

    response ▸ {
                 "focus_time":  3_600,
                 "sessions":    2
               }
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        qs = Vimo.objects.filter(user=request.user, created_at__date=today)
        balance = Vimo.objects.filter(user=request.user)

        data = qs.aggregate(
            focus_time = Sum("focus_time"),
            sessions   = Sum("session"),
        )
        data["balance"] = balance.aggregate(balance=Sum("balance"))
        # Replace None with 0 so front-end never sees null
        data = {k: data.get(k) or 0 for k in data}
        return Response(data, status=status.HTTP_200_OK)
    

# ═══════════════════════════════════════════════════════════════════════════════
# Notes API Views
# ═══════════════════════════════════════════════════════════════════════════════

class NoteListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/notes/           → list all notes for the authenticated user
    POST /api/notes/           → create a new note

    POST body ▸ {
                   "title": "My Note Title",
                   "content": "Note content here..."
                 }
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/notes/<id>/    → retrieve a specific note
    PUT    /api/notes/<id>/    → update a specific note
    PATCH  /api/notes/<id>/    → partial update a specific note
    DELETE /api/notes/<id>/    → delete a specific note

    PUT/PATCH body ▸ {
                        "title": "Updated Title",
                        "content": "Updated content..."
                     }
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    