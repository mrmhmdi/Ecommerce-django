from django.shortcuts import render
from django.views.generic import DetailView

from .models import Product
# Create your views here.


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
