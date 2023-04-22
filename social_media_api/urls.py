from django.urls import path, include
from rest_framework import routers


from social_media_api.views import PostViewSet, LikeViewSet, CommentViewSet, \
    FollowViewSet, FollowUser

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)
router.register("comments", CommentViewSet)
router.register("follows", FollowViewSet)


app_name = "social_media_api"

urlpatterns = [
    path("", include(router.urls)),
    path("follow/<int:id>/", FollowUser.as_view(), name="follow"),
]

