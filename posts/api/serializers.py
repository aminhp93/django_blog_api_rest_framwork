from rest_framework.serializers import (
	ModelSerializer, 
	HyperlinkedIdentityField, 
	SerializerMethodField
	)

from posts.models import Post

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
	url = post_detail_url
	user = SerializerMethodField()
	image = SerializerMethodField()
	markdown = SerializerMethodField()

	def get_user(self, obj):
		return str(obj.user.username)

	def get_image(self, obj):
		try:
			image = obj.image.path
		except:
			image = None
		return image

	def get_markdown(self, obj):
		return obj.get_markdown()

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
		]

class PostListSerializer(ModelSerializer):
	url = post_detail_url

	delete_url = HyperlinkedIdentityField(
		view_name = "posts-api:delete",
		lookup_field = "slug"
		)
	user = SerializerMethodField()

	def get_user(self, obj):
		return str(obj.user.username)

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