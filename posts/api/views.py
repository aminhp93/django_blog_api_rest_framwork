from rest_framework.generics import (
	CreateAPIView,
	ListAPIView, 
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	)

from posts.models import Post

from .serializers import (
	PostListSerializer, 
	PostDetailSerializer, 
	PostCreateUpdateSerializer
	)

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer

class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = "slug"
	# lookup_url_kwarg = "abc"

class PostUpdateAPIView(UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = "slug"

class PostDestroyAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = "slug"