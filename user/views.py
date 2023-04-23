from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import (
    UserSerializer,
    TokenSerializer,
    PartialUserSerializer,
)

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class TokenLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PartialUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PartialUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        email = self.request.query_params.get("email")
        first_name = self.request.query_params.get("first_name")
        if email:
            queryset = queryset.filter(email__icontains=email)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        return queryset


class UserProfileDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            profile = User.objects.get(id=self.request.user.id)
            return profile
        except User.DoesNotExist:
            raise NotFound("Profile does not exist")

    def delete(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.delete()
        return Response({"detail": "Profile has been deleted."})
