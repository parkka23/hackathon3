from rating.serializers import ReviewSerializer
from . import serializers
from .models import Favourites, Post, Comment, Like
from .permissions import IsOwner
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


# Create your views here.

class StandardResultPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('owner', 'category', )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category', 'owner')
    search_fields = ('title',)
    pagination_class = StandardResultPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return serializers.PostDetailSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        else:
            return serializers.PostListSerializer

    def get_permissions(self):
        if self.action in ('create', 'add_to_liked', 'favourite_action'):
            return [permissions.IsAuthenticated()]
        elif self.action in ('update', 'partial_update', 'destroy', 'get_likes'):
            return [permissions.IsAuthenticated(), IsOwner()]
        else:
            return [permissions.AllowAny()]

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        post = self.get_object()
        if request.user.liked.filter(post=post).exists():
            request.user.liked.filter(post=post).delete()
            return Response('You deleted the like', status=204)
        Like.objects.create(post=post, owner=request.user)
        return Response('You liked the post', status=201)

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST'], detail=True)
    def favourite_action(self, request, pk):
        post = self.get_object()
        if request.user.favourites.filter(post=post).exists():
            request.user.favourites.filter(post=post).delete()
            return Response('This post is deleted from Favourites', status=204)
        Favourites.objects.create(post=post, owner=request.user)
        return Response('This post is added to Favourites', status=201)

    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        post = self.get_object()
        if request.method == 'GET':
            reviews = post.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return Response(serializer, status=200)
        data = request.data
        serializer = ReviewSerializer(
            data=data, context={'request': request, 'post': post})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)
