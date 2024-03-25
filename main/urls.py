from django.urls import path
from . import views


urlpatterns = [
    path('', views.products_view, name='products'),
    path('product/<int:id>/', views.product_view, name='product'),
    path(
        'product/<int:id>/add/',
        views.add_to_basket_view,
        name='add_to_basket'
    ),
    path('basket/', views.basket_view, name='basket'),
    path('basket/clear/', views.basket_clear_view, name='basket_clear'),
]
