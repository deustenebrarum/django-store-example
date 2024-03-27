# Generated by Django 5.0.2 on 2024-03-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products')),
                ('description', models.TextField(blank=True, default='', verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена')),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Цена без скидки(зачеркнуто)')),
                ('count', models.IntegerField(default=0, verbose_name='Количество')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
