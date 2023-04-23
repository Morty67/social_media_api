from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response

from .models import (
    Post,
    Like,
    Follow,
    Comment,
)
from .permissions import IsAuthorOrReadOnly

from .serializers import (
    PostSerializer,
    LikeSerializer,
    FollowSerializer,
    CommentSerializer,
    FollowAddSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = Post.objects.all()
        content = self.request.query_params.get("content")
        authors = self.request.query_params.get("author")
        if content:
            queryset = queryset.filter(content__icontains=content)
        if authors:
            authors_id = self._params_to_ints(authors)
            queryset = queryset.filter(author_id__in=authors_id)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "You are not authorized to update this post."},
                status=403,
            )


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )
    # permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
   # permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FollowUser(generics.CreateAPIView):
    serializer_class = FollowAddSerializer

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
