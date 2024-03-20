from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Product


def products_view(request: HttpRequest):
    products = Product.objects.filter(is_active=True)
    products = products.order_by('-count')

    return HttpResponse(render(request, 'products.html', {
        'products': products
    }))


def get_product_for_view(id: int):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404('Товар не найден')

    if not product.is_active:
        raise Http404('Товар не доступен')

    return product


def product_view(request: HttpRequest, id: int):
    return HttpResponse(render(request, 'product.html', {
        'product': get_product_for_view(id=id)
    }))


def add_to_basket_view(request: HttpRequest, id: int):
    product = get_product_for_view(id=id)

    if product.count < 1:
        return redirect('product', id=id)

    request.session['basket'] = request.session.get('basket', []) + [
        {
            'product_id': id,
            'quantity': 1
        }
    ]

    return redirect('products')


def basket_view(request: HttpRequest):
    items = request.session.get('basket', [])

    for item in items:
        item['product'] = Product.objects.get(id=item['product_id'])

    return HttpResponse(render(request, 'basket.html', {
        'items': items
    }))
