from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from posts.models import Post, Group, User
from .permissions import AuthorOrReadOnly, FollowAuthorOrReadOnly
from .serializers import (
    PostSerializer, UserSerializer, CommentSerializer,
    FollowSerializer, GroupSerializer)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import mixins


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        posts = get_object_or_404(Post, id=post_id)
        new_queryset = posts.comments.select_related('post')
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (FollowAuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        new_queryset = self.request.user.follower
        return new_queryset

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
