from urllib import request
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, TemplateView
from .models import Cart, CartItem
from products.models import Product
# Create your views here.


class AddToCartItem(View):

    def get(self, request, slug):
        cart, created_cart = Cart.objects.get_or_create(
            user=request.user, completed=False)
        product = get_object_or_404(Product, slug=slug)
        cartitem, created_item = CartItem.objects.update_or_create(
            cart=cart, product=product, price_ht=product.price
        )

        if not created_item:
            quantity = cartitem.quantity
            cartitem.quantity = quantity+1
            cartitem.save()
        return render(request, 'carts/menu_cart.html')


class CartItemListView(ListView):
    template_name = 'carts/cart_page.html'
    context_object_name = 'cart'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).prefetch_related('product')


class CheckOutTemplateView(TemplateView):
    template_name = 'carts/checkout_page.html'
