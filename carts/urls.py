from django.urls import path

from .views import AddToCartItem

urlpatterns = [
    path('<slug:slug>', AddToCartItem.as_view(), name='add_to_cart')
]
