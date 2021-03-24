from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Comment, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializers, PostSerializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """ Переопределяем функцию, сохраняем поле автора"""
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def list(self, request, post_id=None):
        """Собираем коменты по id поста и прогоняем через сериализатор"""
        post = get_object_or_404(Post, pk=post_id)
        queryset = post.comments.all()
        serializers = CommentSerializers(queryset, many=True)
        return Response(serializers.data)

    def perform_create(self, serializer):
        """ Переопределяем функцию, сохраняем поле автора"""
        serializer.save(author=self.request.user)
