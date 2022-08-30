from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from products.models import Product
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def total_price(self):
        return sum(price.total_price for price in self.cartitem.all())

    def __str__(self) -> str:
        return str(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cartitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(blank=True)

    class Meta:
        unique_together = (('cart', 'product'))

    def get_absolute_url(self):
        return reverse("product_quantity", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cart.user} {self.product}'
