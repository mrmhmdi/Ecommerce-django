from .models import Cart


def cart_globally(request):
    if request.user.is_authenticated:
        cart, created_cart = Cart.objects.get_or_create(
            user=request.user, completed=False)
        return {'cart_g': cart.cartitem.all()}
    else:
        return {'cart_g': {}}
