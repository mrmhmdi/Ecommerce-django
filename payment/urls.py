from django.urls import path

from .views import go_to_gateway_view, callback_gateway_view

urlpatterns = [
    path('go-to-bank-gateway/', go_to_gateway_view, name='bank-gateway'),
    path('callback-gateway/', callback_gateway_view, name='callback-gateway')
]
