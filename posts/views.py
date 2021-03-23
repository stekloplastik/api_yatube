from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from posts.permissions import IsAuthorOrReadOnly
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializers, CommentSerializers
from .permissions import IsAuthorOrReadOnly, IsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        """ Переопределяем функцию, сохраняем поле автора"""
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def list(self, request, post_id=None):
        """Собираем коменты по id поста и прогоняем через сериализатор"""
        post = get_object_or_404(Post, pk=post_id)
        queryset = post.comments.all()
        serializers = CommentSerializers(queryset, many=True)
        return Response(serializers.data)

    def perform_create(self, serializer):
        """ Переопределяем функцию, сохраняем поле автора"""
        serializer.save(author=self.request.user)
