from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from social_media_api.views import (
    FollowUser,
    FollowUserRemove,
    MyPostsView,
    FollowingPostsView,
    LikeCreateAPIView,
    LikeDestroyAPIView,
)
from .views import (
    CreateUserView,
    ManageUserView,
    PartialUserUpdateAPIView,
    UserListAPIView,
    UserProfileDeleteView,
    LogoutView,

)

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("token/logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("me", ManageUserView.as_view(), name="manage"),
    path("me/update", PartialUserUpdateAPIView.as_view(),
         name="me-update"),
    path("me/delete/", UserProfileDeleteView.as_view(),
         name="me-delete"),
    path("follow/<int:id>/", FollowUser.as_view(), name="follow"),
    path(
        "follow/<int:id>/remove/",
        FollowUserRemove.as_view(),
        name="unfollow",
    ),
    path(
        "post/<int:pk>/like",
        LikeCreateAPIView.as_view(),
        name="post-like",
    ),
    path(
        "post/<int:pk>/dislike",
        LikeDestroyAPIView.as_view(),
        name="post-like-delete",
    ),
    path("my-posts/", MyPostsView.as_view(), name="my-posts"),
    path("follow-posts/", FollowingPostsView.as_view(), name="posts-follow"),
]
