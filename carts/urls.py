from django.urls import path

from .views import AddToCartItem, CartItemListView, CheckOutTemplateView

urlpatterns = [
    path('<slug:slug>', AddToCartItem.as_view(), name='add_to_cart'),
    path('cartpage/', CartItemListView.as_view(), name='cartpage'),
    path('checkout/', CheckOutTemplateView.as_view(), name='checkout_page')
]
