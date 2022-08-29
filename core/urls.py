from django.urls import path

from .views import AccountTemplateView, EditAccountView, HomePageListView, ShopView

urlpatterns = [
    path('', HomePageListView.as_view(), name='homepage'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('myaccount/', AccountTemplateView.as_view(), name='myaccount'),
    path('edit-myaccount/<slug:pk>/',
         EditAccountView.as_view(), name='edit_myaccount')
]
