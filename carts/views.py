from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cart, CartItem
from products.models import Product
# Create your views here.


class AddToCartItem(View):

    def get(self, request, slug):
        cart, created_cart = Cart.objects.get_or_create(
            user=request.user, completed=False)
        product = get_object_or_404(Product, slug=slug)
        cartitem, created_item = CartItem.objects.update_or_create(
            cart=cart, product=product)

        if not created_item:
            quantity = cartitem.quantity
            cartitem.quantity = quantity+1
            cartitem.save()
        return render(request, 'carts/menu_cart.html')


class ProductQuantityView(View):

    def get(self, request, pk):
        cartitem = get_object_or_404(CartItem, id=pk)
        action = request.GET.get('increment')
        response = render(request, 'carts/item_quantity.html',
                          {'cartitem': cartitem})

        if action == 'True':
            cartitem.quantity += 1
        else:
            cartitem.quantity -= 1
            if cartitem.quantity <= 0:
                cartitem.delete()
                return response
        cartitem.save()
        return response


class CartItemListView(LoginRequiredMixin, ListView):
    template_name = 'carts/cart_page.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).prefetch_related('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = get_object_or_404(
            Cart, user=self.request.user, completed=False).total_price()
        return context


class CheckOutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'carts/checkout_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = get_object_or_404(
            Cart, user=self.request.user, completed=False).total_price()
        return context
