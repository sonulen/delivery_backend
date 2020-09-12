from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProductSets(models.Model):
    """Набор продуктов"""
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)


class Recipient(models.Model):
    """Получатель"""
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=15)
    delivery_address = models.CharField(max_length=256)


class Order(models.Model):
    """Заказ"""

    class OrderStatus(models.TextChoices):
        """Статус заказа"""
        CREATED = 'Created', _('Создан')
        DELIVERED = 'Delivered', _('Доставлен')
        PROCESSED = 'Processed', _('Обработан')
        CANCELLED = 'Cancelled', _('Отменен')

    order_created_datetime = models.DateTimeField(auto_now_add=True)  # дата и время создания заказа
    delivery_datetime = models.DateTimeField()  # дата и время доставки
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='recipient')  # Получатель
    product_set = models.ForeignKey(ProductSets, on_delete=models.PROTECT, related_name='products')  # Набор продуктов
    status = models.CharField(
        max_length=24,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED)  # Статус заказа
