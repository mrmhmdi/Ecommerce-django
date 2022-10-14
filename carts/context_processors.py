from .models import Cart


def cart_globally(request):
    if request.user.is_authenticated:
        cart, created_cart = Cart.objects.get_or_create(
            user=request.user, completed=False)
        query = cart.cartitem.all()
        total_quantity = 0
        for item in query:
            total_quantity += item.quantity
        return {'cart_g': query, 'total_quantity': total_quantity}
    else:
        return {'cart_g': {}}
