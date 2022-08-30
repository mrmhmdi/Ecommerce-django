from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class CreateOrder(TemplateView):
    template_name = 'order/checkout_page.html'
