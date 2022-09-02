from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from products.models import Product
# Create your models here.


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        ORDERD = 'OR'
        SHIPPED = 'SP'
        DELIVERD = 'DD'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    zip_code = models.CharField(max_length=25, blank=False)
    place = models.CharField(max_length=255, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False,)
    total_price = models.IntegerField(default=0)
    status = models.CharField(
        max_length=2, choices=OrderStatus.choices, default=OrderStatus.ORDERD)

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(
        validators=[phoneNumberRegex], max_length=16, blank=False)
    tracking_code = models.PositiveBigIntegerField(default=0000)
    paid_amount = models.PositiveIntegerField(default=0000)

    class Meta:
        ordering = ('-create_at',)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
