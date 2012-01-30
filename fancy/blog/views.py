from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import date
from models import Post,Category
from taggit.models import Tag

def index(request):
	category_list = Category.objects.all()
	
	return render_to_response('fancy/blog/index.html', 
		{ 'category_list' : category_list },context_instance=RequestContext(request))

def detail(request,slug):
	post = get_object_or_404(Post,slug=slug)
	
	if post.redirect_to:
	    return redirect(post.redirect_to)
	
	return render_to_response('fancy/blog/detail.html',{'post':post},
                                  context_instance=RequestContext(request))

def show_post_list(request,post_list,title="",archieve_type="category"):
	paginator = Paginator(post_list, 50)
	page = int(request.GET.get('page', '1'))
	
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1
		
	try:
		posts = paginator.page(page)
	except (EmptyPage, InvalidPage):
		posts = paginator.page(paginator.num_pages)

	return render_to_response('fancy/blog/posts.html', { 
						'post_list' : posts, 
						'title' : title,
						'archieve_type' : archieve_type
						}, context_instance=RequestContext(request) )

def tag_index(request,slug):
	tag = get_object_or_404(Tag,slug=slug)
	post_list = Post.objects.filter(tags__slug__in=[slug.lower()],status=1)
	title = tag.name
	return show_post_list(request,post_list,title,'tag')

def category_index(request,slug):
	category = get_object_or_404(Category,slug=slug)
	post_list = Post.objects.filter(categories=category,status=1)
	title = category.name
	return show_post_list(request,post_list,title,'category')

def year_index(request,year):
	post_list=Post.objects.filter(date__year=year,status=1)
	title = date( int(year), 1, 1)
	return show_post_list(request,post_list,title,"year")
		
def month_index(request,year,month):
	post_list=Post.objects.filter(date__year=year, date__month=month,status=1) 
	title = date( int(year), int(month), 1)
	return show_post_list(request,post_list,title,"month")
	
	
	


	