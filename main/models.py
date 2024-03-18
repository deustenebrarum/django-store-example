from django.db import models


class Product(models.Model):
    title = models.CharField(
        max_length=255, blank=False, verbose_name='Название'
    )
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Цена'
    )
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        verbose_name='Цена со скидкой'
    )
    count = models.IntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title
