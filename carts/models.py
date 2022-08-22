from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cartitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True)

    class Meta:
        unique_together = (('cart', 'product'))

    TAX_AMOUNT = 10

    def price_ttc(self):
        return self.price_ht * (1 + self.TAX_AMOUNT / 100)

    def __str__(self):
        return f'{self.cart.user} {self.product}'
