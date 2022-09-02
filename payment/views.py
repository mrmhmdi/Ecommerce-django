import logging

from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException

from order.models import Order
# Create your views here.


def go_to_gateway_view(request):
    pk = request.GET.get('ord-pk')
    order = get_object_or_404(Order, user=request.user, id=pk)
    if order.paid == True:
        return Http404
    amount = order.total_price

    factory = bankfactories.BankFactory()
    try:
        # or factory.create(bank_models.BankType.BMI) or set identifier
        bank = factory.auto_create()
        bank.set_request(request)
        bank.set_amount(amount)
        # URL back to the software to continue the process
        bank.set_client_callback_url(reverse('callback-gateway'))

        # Set the tracking code in order for tarck the peyment later
        bank_record = bank.ready()
        order.tracking_code = bank_record.tracking_code
        order.save()

        # Directing the user to the bank gateway
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug('This link is not valid.')
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug('This link is not valid.')
        raise Http404

    # In this section, we must perform the corresponding record or any other appropriate action
    # through the data in the record bank.
    if bank_record.is_success:
        order = get_object_or_404(Order, tracking_code=tracking_code)
        order.paid_amount = bank_record.amount
        if float(bank_record.amount) == float(order.total_price):
            order.paid = True
        order.save()
        return render(request, 'payment/success.html')

    # Payment has not been successful.
    return render(request, 'payment/failed.html')
