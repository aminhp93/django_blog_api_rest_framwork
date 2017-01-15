from rest_framework.serializers import (
	ModelSerializer, 
	HyperlinkedIdentityField, 
	SerializerMethodField
	)

from posts.models import Post

from comments.api.serializers import CommentListSerializer
from comments.models import Comment

from accounts.api.serializers import UserDetailSerialzier

class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'publish',
		]

post_detail_url = HyperlinkedIdentityField(
		view_name = 'posts-api:detail',
		lookup_field = 'slug',
		)

class PostDetailSerializer(ModelSerializer):
	user = UserDetailSerialzier()
	url = post_detail_url
	# user = SerializerMethodField()
	image = SerializerMethodField()
	markdown = SerializerMethodField()
	comments = SerializerMethodField()

	# def get_user(self, obj):
	# 	return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.path
		except:
			image = None
		return image

	def get_markdown(self, obj):
		return obj.get_markdown()

	def get_comments(self, obj):
		# content_type = obj.get_content_type
		# object_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)
		comments = CommentListSerializer(c_qs, many=True).data
		return comments


	class Meta:
		model = Post
		fields = [
			'image',
			'user',
			'url',
			'id',
			'title',
			'slug',
			'content',
			'publish',
			'markdown',
			'comments',
		]

class PostListSerializer(ModelSerializer):
	user = UserDetailSerialzier()
	url = post_detail_url

	delete_url = HyperlinkedIdentityField(
		view_name = "posts-api:delete",
		lookup_field = "slug"
		)
	# user = SerializerMethodField()

	# def get_user(self, obj):
	# 	return str(obj.user.username)

	class Meta:
		model = Post
		fields = [
			'url',
			'user',
			'title',
			# 'slug',
			'content',
			'publish',
			'delete_url',
		]