from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import date
from models import Post, Category
from taggit.models import Tag


def index(request):
    category_list = Category.objects.all()
    latest_posts = Post.objects.filter(status=Post.PUB_STATUS_PUBLISHED)[:10]

    return render(request, 'fancy/blog/index.html', {
        'category_list': category_list,
        'latest_posts': latest_posts
    })


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.PUB_STATUS_PUBLISHED)

    if post.redirect_to:
        return redirect(post.redirect_to)

    return render(request, 'fancy/blog/detail.html', {'post': post})


def show_post_list(request, post_list, title="", archieve_type="category"):
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

    return render(
        request,
        'fancy/blog/posts.html',
        {
            'post_list': posts,
            'title': title,
            'archieve_type': archieve_type
        }
    )


def tag_index(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post_list = Post.objects.filter(tags__slug__in=[slug.lower()],
                                    status=Post.PUB_STATUS_PUBLISHED)
    title = tag.name
    return show_post_list(request, post_list, title, 'tag')


def category_index(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post_list = Post.objects.filter(categories=category,
                                    status=Post.PUB_STATUS_PUBLISHED)
    title = category.name
    return show_post_list(request, post_list, title, 'category')


def year_index(request, year):
    post_list = Post.objects.filter(date__year=year,
                                    status=Post.PUB_STATUS_PUBLISHED)
    title = date(int(year), 1, 1)
    return show_post_list(request, post_list, title, "year")


def month_index(request, year, month):
    post_list = Post.objects.filter(date__year=year,
                                    date__month=month,
                                    status=Post.PUB_STATUS_PUBLISHED)
    title = date(int(year), int(month), 1)
    return show_post_list(request, post_list, title, "month")
