from django.views.generic import ListView
from django.db.models import Q

from products.models import Product, Category
# Create your views here.


class HomePageListView(ListView):
    model = Product
    template_name = 'core/core.html'
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset()[:8]


class ShopView(ListView):
    model = Product
    template_name = 'core/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = super().get_queryset()
        if category := self.request.GET.get('cat', default=''):
            query = Product.objects.filter(
                category__slug__icontains=category)
        if search_input := self.request.GET.get('q', default=''):
            query = Product.objects.filter(
                Q(name__icontains=search_input) | Q(description__icontains=search_input))

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context['active_category'] = self.request.GET.get('cat', default='')
        return context
