from .models import Cart
from django.shortcuts import get_object_or_404, HttpResponse


def cart_globally(request):
    if request.user.is_authenticated:
        cart, created_cart = Cart.objects.get_or_create(
            user=request.user, completed=False)
        return {'cart_g': cart.cartitem.all()}
    else:
        return {'cart_g': {}}