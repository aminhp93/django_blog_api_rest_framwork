from django.db.models import Q

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from posts.models import Post

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

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
	# IsAuthenticatedOrReadOnly,
	)

from comments.models import Comment

from .serializers import (
	CommentListSerializer,
	CommentDetailSerializer,
	# CommentEditSerializer,
	create_comment_serializer
	)

class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	# serializer_class = CommentCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]

	# def perform_create(self, serializer):
		# serializer.save(user=self.request.user)
	def get_serializer_class(self):
		model_type = self.request.GET.get("type")
		slug = self.request.GET.get("slug")
		parent_id = self.request.GET.get("parent_id", None)
		return create_comment_serializer(
			model_type="post",
			slug=slug,
			parent_id = parent_id,
			user = self.request.user
			)


class CommentListAPIView(ListAPIView):
	# queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ["content", "user__first_name"]
	pagination_class = PostPageNumberPagination
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):
		# queryset_list = super().get_queryset(*args, **kwargs)
		queryset_list = Comment.objects.filter(id__gte=0)
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query) 
				).distinct()
		return queryset_list

class CommentDetailAPIView(DestroyAPIView, UpdateAPIView, RetrieveAPIView):
	queryset = Comment.objects.filter(id__gte=0)
	serializer_class = CommentDetailSerializer
	permission_classes = [IsOwnerOrReadOnly]


	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

