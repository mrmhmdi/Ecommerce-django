from django.urls import path

from .views import CreateOrder

urlpatterns = [
    path('', CreateOrder.as_view(), name='order'),
]
