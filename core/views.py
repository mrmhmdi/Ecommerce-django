from django.views.generic import ListView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.http.response import HttpResponseBadRequest

from products.models import Product, Category
from order.models import Order
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


class AccountTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'core/myaccount.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user_obj'] = user
        context['orders'] = Order.objects.filter(
            user=user).prefetch_related('orderitem')
        return context


class EditAccountView(LoginRequiredMixin, UpdateView):
    template_name = 'core/edit_myaccount.html'
    fields = ('first_name', 'last_name', 'username', 'email', )
    context_object_name = 'user_obj'
    http_method_names = ('get', 'post')

    def get(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.username:
            return HttpResponseBadRequest("Bad Request")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.username:
            return HttpResponseBadRequest("Bad Request")
        return super().post(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def get_success_url(self) -> str:
        return reverse('myaccount')
