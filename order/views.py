from django.shortcuts import redirect, render
from django.views import View

from .forms import OrderModelForm
from .models import OrderItem
from carts.models import CartItem
# Create your views here.


class CreateOrder(View):
    def get(self, request):
        return render(request, 'order/checkout_page.html', {'price': request.GET.get('price')})

    def post(self, request):
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
        cartitems = CartItem.objects.filter(
            cart__user=request.user, cart__completed=False).prefetch_related('cart')
        for item in cartitems:
            orderitem = OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.total_price,
                quantity=item.quantity
            )
        else:
            cart = item.cart
            cart.completed = True
            cart.save()
        return redirect('myaccount')
