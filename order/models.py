from statistics import quantiles
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
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=25)
    place = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amaount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=2, choices=OrderStatus.choices, default=OrderStatus.ORDERD)

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(
        validators=[phoneNumberRegex], max_length=16, unique=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantiles = models.PositiveIntegerField(default=1)
