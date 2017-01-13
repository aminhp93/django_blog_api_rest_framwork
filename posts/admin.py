from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'title' ,'update', 'timestamp')
	list_display_link = ('update')
	list_editable = ['title']
	list_filter = ['update', 'timestamp']

	search_fields = ['title', 'content']
	class Meta:
		model = Post

admin.site.register(Post, PostAdmin)
