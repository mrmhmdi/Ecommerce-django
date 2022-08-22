from .models import Cart
from django.shortcuts import get_object_or_404


def cart_globally(request):
    cart = get_object_or_404(Cart, user=request.user, completed=False)
    return {'cart_g': cart.cartitem.all()}
