from django.contrib import admin
from django.utils.html import format_html_join, format_html
from django.urls import reverse

from .models import Category, Order, OrderProduct, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'categories')

    fields = ('title', 'categories', 'description',
              'price', 'original_price', 'count', 'is_active', 'image', 'created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')

    search_fields = ('title', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    list_filter = ('parent', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('_id', 'user', 'status', 'total_price',
                    'created_at', 'updated_at')

    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name'
    )

    fields = ('user', 'status', '_id', 'total_price', 'display_order_products')

    readonly_fields = ('display_order_products', '_id', 'total_price')

    list_filter = ('status', 'created_at', 'updated_at')

    actions = ['cancel_order', 'set_payed', 'set_in_progress']

    @admin.display(description='Товары в заказе:')
    def display_order_products(self, obj):
        products_data = [
            (
                reverse(
                    'admin:main_product_change',
                    args=[str(order_product.product.id)]
                ),
                f'{order_product.product.title} ' +
                f'({order_product.quantity}) * ' +
                f'{order_product.price} = ' +
                f'{order_product.price * order_product.quantity}'
            )
            for order_product in OrderProduct.objects.filter(order=obj)
        ]

        list_elements = format_html_join(
            '',
            '<li><a href="{}">{}</a></li>',
            products_data
        )

        list_styles = '''
            list-style-type:none;
            padding: 0;
            margin: 0;
            font-weight: bold;
        '''

        return format_html(
            '<ul style="{}">{}</ul>',
            list_styles, list_elements
        )

    def cancel_order(self, request, queryset):
        queryset.update(status=Order.Status.CANCELED)
    cancel_order.short_description = 'Отменить выбранные заказы'

    def set_payed(self, request, queryset):
        queryset.update(status=Order.Status.PAYED)
    set_payed.short_description = 'Сделать заказы оплаченными'

    def set_in_progress(self, request, queryset):
        queryset.update(status=Order.Status.IN_PROGRESS)
    set_in_progress.short_description = 'Сделать заказы в обработке'

    @admin.display(description='№')
    def _id(self, obj):
        return obj.pk

    @admin.display(description='Сумма')
    def total_price(self, obj):
        return obj.total_price
