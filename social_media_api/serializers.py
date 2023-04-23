from rest_framework import serializers

from social_media_api.models import (
    Comment,
    Post,
    Like,
    Follow,
)


class CommentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    # post = PostSerializer()

    class Meta:
        model = Comment
        fields = (
            "email",
            "post",
            "content",
            "created_at",
        )


class PostSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    likes = serializers.SerializerMethodField()
    media = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "created_at",
            "email",
            "likes",
            "media",
        )

    def get_likes(self, obj):
        return [like.user.email for like in obj.likes.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("user", None)
        return representation


class LikeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    post = PostSerializer()

    class Meta:
        model = Like
        fields = ("id", "post", "email")


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "id",
            "created_at",
            "follower",
            "following",
        )

    def get_follower(self, follow):
        return follow.follower.email

    def get_following(self, follow):
        return follow.following.email

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FollowAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "following")


class FollowRemoveSerializer(serializers.Serializer):
    following_id = serializers.IntegerField()

    def validate_following_id(self, value):
        try:
            Follow.objects.get(
                following_id=value,
                follower=self.context["request"].user,
            )
        except Follow.DoesNotExist:
            raise serializers.ValidationError(
                "You are not following this user.",
            )
        return value

    def delete(self):
        following_id = self.validated_data["following_id"]
        follower = self.context["request"].user
        follow_obj = Follow.objects.filter(
            following_id=following_id,
            follower=follower).first()
        if follow_obj:
            follow_obj.delete()


class OwnPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class FollowPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_likes(self, obj):
        return obj.likes.count()
