from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    CreateUserView,
    ManageUserView,
    TokenLogoutView,
    PartialUserUpdateAPIView,
    UserListAPIView,

)

app_name = "user"

urlpatterns = [
    path("register", CreateUserView.as_view(), name="create"),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("token/logout", TokenLogoutView.as_view(), name="token_logout"),
    path("me", ManageUserView.as_view(), name="manage"),
    path("me/update", PartialUserUpdateAPIView.as_view(),
         name="me-update"),
    path("users", UserListAPIView.as_view(), name="user-list"),
]
