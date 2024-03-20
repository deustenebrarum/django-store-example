from django.urls import path
from . import views


urlpatterns = [
    path('', views.products_view, name='index'),
    path('product/<int:id>/', views.product_view, name='product'),
]
