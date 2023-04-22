from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(many=True, read_only=True)
    following = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "password",
            "email",
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "follower",
            "following",
        )
        read_only_fields = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "avatar",
            "bio",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs["refresh"]

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Token is invalid or expired")

        return attrs


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "bio",
            "avatar",
        )
