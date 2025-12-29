from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name", "role")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = getattr(user, "role", None)
        token["username"] = user.get_username()
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data["user"] = UserSerializer(self.user).data
            return data
        except Exception as e:
            # If it's already a ValidationError, re-raise it
            if isinstance(e, serializers.ValidationError):
                raise e
            # Otherwise, log it and raise a generic error to avoid 500
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Login validation error: {str(e)}", exc_info=True)
            raise serializers.ValidationError({"detail": f"An error occurred during login: {str(e)}"})