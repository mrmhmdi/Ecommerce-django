from django.urls import path

from .views import (AddToCartItem, CartItemListView,
                    ProductQuantityView,)

urlpatterns = [
    path('', CartItemListView.as_view(), name='cartpage'),
    path('add-to-cart/<slug:slug>/', AddToCartItem.as_view(), name='add_to_cart'),
    path('quantity/<slug:pk>/', ProductQuantityView.as_view(),
         name='product_quantity'),
]
