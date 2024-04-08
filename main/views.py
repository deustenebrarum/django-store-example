from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Order, OrderProduct, Product
from .forms import SearchForm


def products_view(request: HttpRequest):
    products = Product.objects.filter(is_active=True)
    products = products.order_by('-count')

    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        products = products.filter(
            title__icontains=search_form.cleaned_data['query']
        )

    return HttpResponse(render(request, 'products.html', {
        'products': products,
        'search_form': search_form
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


def basket_add_view(request: HttpRequest, id: int):
    product = get_product_for_view(id=id)

    if product.count < 1:
        return redirect('product', id=id)

    basket: list = request.session.get('basket', [])

    found_item = next(
        (item for item in basket if item['product_id'] == id),
        None,
    )

    if found_item is not None:
        found_item['quantity'] = found_item['quantity'] + 1
    else:
        basket.append({
            'product_id': id,
            'quantity': 1
        })

    request.session['basket'] = basket

    return redirect('basket')


def basket_increase_view(request: HttpRequest, id: int):
    items = request.session.get('basket', [])
    product = get_product_for_view(id=id)

    found_item = next(
        (item for item in items if item['product_id'] == id),
        None,
    )

    if found_item is None:
        raise Http404('Товар не найден')

    if product.count < found_item['quantity'] + 1:
        raise HttpRequest('Товар закончился', status=400)

    found_item['quantity'] = found_item['quantity'] + 1

    request.session['basket'] = items

    return HttpResponse(status=200)


def basket_view(request: HttpRequest):
    items = request.session.get('basket', [])

    for item in items:
        item['product'] = Product.objects.get(id=item['product_id'])

    total_price = sum(item['product'].price * item['quantity']
                      for item in items)

    return HttpResponse(render(request, 'basket.html', {
        'items': items,
        'total_price': total_price,
    }))


def basket_clear_view(request: HttpRequest):
    request.session.update({'basket': []})

    return redirect('basket')


def basket_decrease_view(request: HttpRequest, id: int):
    items = request.session.get('basket', [])

    found_item = next(
        (item for item in items if item['product_id'] == id),
        None,
    )

    if found_item is None:
        raise Http404('Товар не найден')

    if found_item['quantity'] > 1:
        found_item['quantity'] = found_item['quantity'] - 1
    else:
        items.remove(found_item)

    request.session['basket'] = items

    return HttpResponse(status=200)


@require_http_methods(["POST"])
def order_view(request: HttpRequest):
    if not request.user.is_authenticated:
        login_page = redirect('login')
        login_page['Location'] += '?next=' + reverse('basket')

        return login_page

    if request.method == 'POST':
        order = Order()
        order.user = request.user
        order.save()

        basket = request.session.get('basket', [])

        if len(basket) == 0:
            return redirect('basket')

        for item in basket:
            product = Product.objects.get(id=item['product_id'])
            if item['quantity'] > product.count:
                return HttpResponseBadRequest('Товара не хватает')

        for item in basket:
            order_product = OrderProduct(order=order)
            order_product.product = Product.objects.get(id=item['product_id'])
            order_product.quantity = item['quantity']
            order_product.product.count -= order_product.quantity
            order_product.price = order_product.product.price
            order_product.product.save()
            order_product.save()

        request.session.update({'basket': []})

        return redirect('get_order', id=order.id)


@require_http_methods(["GET"])
def get_order_view(request: HttpRequest, id: int):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        raise Http404('Заказ не найден')

    return HttpResponse(render(request, 'order.html', {
        'order': order,
        'products': OrderProduct.objects.filter(order=order),
    }))
