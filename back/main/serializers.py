from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation
from .models import Vimo, Note


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True, required=True,)
    password2 = serializers.CharField(write_only=True, required=True, label="Repeat password")

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email",)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        # password_validation.validate_password(value, self.context["request"].user)
        return value
    


class VimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vimo
        fields = ("user", "focus_time", "break_time", "session", "balance", "created_at")
        read_only_fields = ("user", "created_at")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "title", "content", "color_index", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        user = self.context["request"].user
        # Auto-assign color_index based on user's existing notes count
        user_notes_count = Note.objects.filter(user=user).count()
        validated_data["color_index"] = user_notes_count % 6
        validated_data["user"] = user
        return super().create(validated_data)
    