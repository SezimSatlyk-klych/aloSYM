from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/",    TokenObtainPairView.as_view(), name="login"),   # returns access + refresh
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/",   LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete_account"),

    path("vimo/create/",        VimoSessionCreateView.as_view(), name="vimo_create"),  # POST
    path("vimo/all/",        VimoAllStatsView.as_view(),     name="vimo_all"),     # GET (same route, different method)
    path("vimo/today/",  VimoTodayStatsView.as_view(),   name="vimo_today"),
    
    # Notes endpoints
    path("notes/", NoteListCreateView.as_view(), name="note_list_create"),  # GET (list) & POST (create)
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="note_detail"),  # GET, PUT, PATCH, DELETE
]
