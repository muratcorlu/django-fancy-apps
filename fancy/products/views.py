from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.http import Http404
from models import Product, Category

def main(request):
    categories = Category.objects.all()
    return direct_to_template(request, 'fancy/products/main.html', {'categories':categories})

def category_main(request, category_slug=None, category_id=None):
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    else:
        raise Http404

    return direct_to_template(request, 'fancy/products/category_main.html', {'category':category})

def detail(request, product_slug=None, product_id=None, category_slug=None):
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
    elif product_slug:
        if category_slug:
            product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
        else:
            product = get_object_or_404(Product, slug=product_slug)
    else:
        raise Http404

    if category_slug and not product.category.slug == category_slug:
        raise Http404

    return direct_to_template(request, 'fancy/products/detail.html', {'product':product})

def main_controller(request, slug):
    parts = request.path_info.strip("/").split("/")
    
    print parts, parts[-1]
    # Check products
    if Product.objects.filter(slug=parts[-1], category__slug=parts[-2]).exists():
        return detail(request, product_slug=parts[-1], category_slug=parts[-2])

    return category_main(request, parts[-1])