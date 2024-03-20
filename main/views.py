from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Product


def products_view(request: HttpRequest):
    products = Product.objects.filter(is_active=True)
    products = products.order_by('-count')

    return HttpResponse(render(request, 'products.html', {
        'products': products
    }))


def product_view(request: HttpRequest, id: int):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404('Товар не найден')

    return HttpResponse(render(request, 'product.html', {
        'product': product
    }))
