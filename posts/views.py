try:
	from urllib import quote_plus
except:
	pass

try:
	from urllib.parse import quote_plus
except:
	pass


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

# from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from .utils import get_read_time


# Create your views here.

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		print(form.cleaned_data.get("title"))
		instance.save()
		messages.success(request, "Successfully Created", extra_tags="some-tag")
		return HttpResponseRedirect(instance.get_absolute_url())

	# if request.method == "POST":
	# 	print(request.POST)
	# 	print(request.POST.get("title"))
		# Post.objects.create(title=title)
	context = {
		"form": form,
	}	
	return render(request, "post_form.html", context)

def post_detail(request, slug=None):
	# instance = Post.objects.get(slug=5)
	instance = get_object_or_404(Post, slug = slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff  or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)

	print(instance.content)
	print(get_read_time(instance.content))
	# content_type = ContentType.objects.get_for_model(Post)
	# obj_id = instance.id
	# comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
	# comments = Comment.objects.filter(post=instance | user = request.user)
	# comments = Comment.objects.filter_by_instance(instance)
	comments = instance.comments

	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id
	}

	form = CommentForm(request.POST or None, initial=initial_data)
	
	if form.is_valid() and request.user.is_authenticated():
		print(form.cleaned_data)
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")

		parent_obj = None

		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id = parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
			user = request.user,
			content_type = content_type,
			object_id = obj_id,
			content = content_data,
			parent = parent_obj,
			)

		if created:
			print("It worked")
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form": form,
	}
	return render(request, 'post_detail.html', context)

def post_list(request):

	queryset_list = Post.objects.all().order_by("-timestamp")
	# queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query) 
			).distinct()

	paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
	page_request_var = "hello"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
			"object_list": queryset,
			"title": "List",
			"page_request_var": page_request_var,
		}
	# if request.user.is_authenticated():

	# 	context = {
	# 		"title": "My user list"
	# 	}
	# else:
	# 	context = {
	# 		"title": "List"
	# 	}

	return render(request, 'post_list.html', context)



def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	# if not request.user.is_authenticated():
		# raise Http404
		
	instance = get_object_or_404(Post, slug = slug)

	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit =False)
		instance.user = request.user
		instance.save()

		messages.success(request, "Successfully saved")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}

	return render(request, 'post_form.html', context)

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")





	


