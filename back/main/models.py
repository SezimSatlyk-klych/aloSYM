from django.db import models as m
from django.conf import settings


class Vimo(m.Model):
    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.CASCADE)
    focus_time = m.IntegerField(default=0)
    break_time = m.IntegerField(default=0)
    session = m.IntegerField(default=0)
    balance = m.IntegerField(default=0)
    created_at = m.DateTimeField(auto_now_add=True)


class Note(m.Model):
    user = m.ForeignKey(settings.AUTH_USER_MODEL, on_delete=m.CASCADE, related_name='notes')
    title = m.CharField(max_length=200)
    content = m.TextField()
    color_index = m.IntegerField(default=0, help_text="Index for note color (0-5)")
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return f"{self.user.username} - {self.title[:50]}"
