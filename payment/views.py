import imp
import logging

from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException

from order.models import Order
# Create your views here.


def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    pk = request.GET.get('ord-pk')
    order = get_object_or_404(Order, user=request.user, id=pk)
    if order.paid == True:
        return Http404
    amount = order.paid_amount

    factory = bankfactories.BankFactory()
    try:
        # or factory.create(bank_models.BankType.BMI) or set identifier
        bank = factory.auto_create()
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('callback-gateway'))

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()
        order.tracking_code = bank_record.tracking_code
        order.save()

        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        order = get_object_or_404(Order, tracking_code=tracking_code)
        if float(bank_record.amount) == float(order.paid_amount):
            order.paid = True
            order.save()
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")


# factory = bankfactories.BankFactory()

# # غیر فعال کردن رکورد های قدیمی
# bank_models.Bank.objects.update_expire_records()

# # مشخص کردن رکوردهایی که باید تعیین وضعیت شوند
# for item in bank_models.Bank.objects.filter_return_from_bank():
#     bank = factory.create(bank_type=item.bank_type,
#                           identifier=item.bank_choose_identifier)
#     bank.verify(item.tracking_code)
#     bank_record = bank_models.Bank.objects.get(
#         tracking_code=item.tracking_code)
#     if bank_record.is_success:
#         logging.debug("This record is verify now.",
#                       extra={'pk': bank_record.pk})
