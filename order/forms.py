from django.forms.models import ModelForm

from .models import Order


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'paid', 'paid_amount', 'status',
                   'tracking_code', 'total_price')
