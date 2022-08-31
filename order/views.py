from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.http.response import HttpResponseBadRequest

from .forms import OrderModelForm
from .models import OrderItem
from carts.models import CartItem, Cart
# Create your views here.


class CreateOrder(View):
    def get(self, request):
        cart = get_object_or_404(
            Cart, user=self.request.user, completed=False)
        if cart.cartitem.all():
            return render(request, 'order/checkout_page.html', {'price': cart.total_price})
        else:
            return redirect('shop')

    def post(self, request):
        cart = get_object_or_404(
            Cart, user=self.request.user, completed=False)
        cartitems = cart.cartitem.select_related('product').all()
        if cartitems:
            form = OrderModelForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
            else:
                return redirect('createorder')

            # create orderitems with submited cartitems
            for item in cartitems:
                orderitem = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.total_price,
                    quantity=item.quantity
                )
            # get the last item in for laop and set the cart to true to create new cart
            else:
                cart = item.cart
                cart.completed = True
                cart.save()
            return redirect('myaccount')
        else:
            return HttpResponseBadRequest('bad request!')
