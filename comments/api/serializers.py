from django.contrib.contenttypes.models import ContentType

from rest_framework.serializers import(
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField,
	ValidationError,
	)

from comments.models import Comment

def create_comment_serializer(model_type='post', slug=None, parent_id = None):
	class CommentCreateSerialer(ModelSerializer):
		class Meta:
			model = Comment
			fields = [
				'id',
				'content',
				'parent',
				'timestamp',
			]

		def __init__(self, *args, **kwargs):
			self.model_type = model_type
			self.slug = slug
			self.parent_obj = None
			if self.parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exist() and parent_qs.count() == 1:
					self.parent_obj = parent_qs.first()
			return super().init(*args, **kwargs)

		def validate(self, data):
			model_type = self.model_type
			model_qs = ContentType.objects.filter(model=model_type)
			if not model_qs.exists() or model_qs.count() != 1:
				raise ValidationError("This is not a valid content type")
			SomeModel = model_qs.first().model_class()
			obj_qs = SomeModel.objects.exists(slug=self.slug)
			if not obj_qs.exists() or obj_qs.count() != 1:
				raise ValidationError("This is not a slug for this content type")
			return data

	return CommentCreateSerializer

class CommentSerializer(ModelSerializer):
	reply_count = SerializerMethodField()

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'content',
			'parent',
			'reply_count',
			'timestamp',
		]

class CommentChildSerializer(ModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'id',
			'content',
			'timestamp',
		]

class CommentDetailSerializer(ModelSerializer):
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	class Meta:
		model = Comment
		fields = [
			'id',
			'content_type',
			'object_id',
			'content',
			'replies',
			'reply_count',
		]