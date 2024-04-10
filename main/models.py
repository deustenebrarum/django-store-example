from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=255, blank=False, verbose_name='Название',
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='Родительская категория'
    )

    @property
    def products(self):
        return Product.objects.filter(category=self)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(
        max_length=255, blank=False, verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='products', null=True, blank=True
    )
    description = models.TextField(
        verbose_name='Описание', default='', blank=True
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Цена'
    )
    original_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name='Цена без скидки(зачеркнуто)'
    )
    count = models.IntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(default=True, verbose_name='Активен?')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class OrderProduct(models.Model):
    order = models.ForeignKey(
        'Order', on_delete=models.CASCADE, verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Товар'
    )
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Цена'
    )

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', 'Создан'
        PAYED = 'PAYED', 'Оплачен'
        IN_PROGRESS = 'IN_PROGRESS', 'В обработке'
        DELIVERING = 'DELIVERING', 'Доставляется'
        DELIVERED = 'DELIVERED', 'Доставлен'
        CANCELED = 'CANCELED', 'Отменен'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    products = models.ManyToManyField(
        Product, verbose_name='Товары',
        through=OrderProduct,
        through_fields=('order', 'product')
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=15, choices=Status.choices, default=Status.CREATED
    )

    @property
    def status_label(self):
        return dict(Order.Status.choices)[self.status]

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )

    @property
    def is_cancelable(self):
        return self.status not in (
            self.Status.CANCELED,
            self.Status.DELIVERED,
            self.Status.DELIVERING
        )

    @property
    def total_price(self):
        return sum([
            order_product.price * order_product.quantity
            for order_product in OrderProduct.objects.filter(order=self)
        ])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order from {str(self.user)}'
