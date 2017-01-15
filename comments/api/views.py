from django.db.models import Q

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from rest_framework.generics import (
	CreateAPIView,
	ListAPIView, 
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	RetrieveUpdateAPIView,
	)

from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)

from comments.models import Comment

from .serializers import (
	CommentSerializer,
	CommentChildSerializer,
	CommentDetailSerializer
	)

# class PostCreateAPIView(CreateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	permission_classes = [IsAuthenticated]

# 	def perform_create(self, serializer):
# 		serializer.save(user=self.request.user)

class CommentListAPIView(ListAPIView):
	# queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ["content", "user__first_name"]
	pagination_class = PostPageNumberPagination

	def get_queryset(self, *args, **kwargs):
		# queryset_list = super().get_queryset(*args, **kwargs)
		queryset_list = Comment.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query) 
				).distinct()
		return queryset_list

class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentDetailSerializer
	# lookup_field = "pk"
	# lookup_url_kwarg = "abc"

# class PostUpdateAPIView(RetrieveUpdateAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostCreateUpdateSerializer
# 	lookup_field = "slug"
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# 	def perform_update(self, serializer):
# 		serializer.save(user=self.request.user)

# class PostDestroyAPIView(DestroyAPIView):
# 	queryset = Post.objects.all()
# 	serializer_class = PostDetailSerializer
# 	lookup_field = "slug"
# 	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

