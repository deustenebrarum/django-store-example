from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Product


def index_view(request: HttpRequest):
    products = Product.objects.filter(is_active=True)

    return HttpResponse(render(request, 'products.html', {
        'products': products
    }))
