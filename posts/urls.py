from django.conf.urls import url

from .views import (post_create, post_detail, post_list, post_update, post_delete)

urlpatterns = [
	url(r'^$', post_list, name='list'),
	url(r'^create/$', post_create, name='create'),
	# url(r'^(?P<id>\d+)/$', post_detail, name='detail'),
	# url(r'^(?P<id>\d+)/edit/$', post_update, name='update'),
	# url(r'^(?P<id>\d+)/delete/$', post_delete, name='delete'),
	url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
	url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
	url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
]