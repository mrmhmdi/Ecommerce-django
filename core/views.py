from django.views.generic import ListView

from products.models import Product
# Create your views here.


class HomePageListView(ListView):
    model = Product
    template_name = 'core/core.html'
    context_object_name = 'products'


class ShopView(ListView):
    model = Product
    template_name = 'core/shop.html'
    context_object_name = 'products'
