from django.urls import path

from .views import HomePageListView, ShopView

urlpatterns = [
    path('', HomePageListView.as_view(), name='homepage'),
    path('shop/', ShopView.as_view(), name='shop')
]
