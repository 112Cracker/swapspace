from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from trade.models import Order
from shoppingCart.models import ShoppingCart
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def payment_done(request):
    return render(request, "payment_done.html")

@csrf_exempt
def payment_canceled(request):
    return render(request, "payment_canceled.html")

def payment_process(request, order_id):
    # order_id = request.session.get('order_id')
    # hardcode to 1
    print(order_id)
    print(type(order_id))
    order = Order.objects.get(id=order_id)
    cart = ShoppingCart.objects.get(user=request.user)
    host = request.get_host()
    items = order.buy_item.all()
    totalprice = 0.00
    for item in items:
        totalprice += float(item.totalprice)
        correspond_sell = item.sell_item
        correspond_sell.amount -= item.incart_amount
        if correspond_sell.amount < 0:
            return render(request, "payment_canceled.html")
        correspond_sell.save()
        cart.buyItem.remove(item)
    print("total price is " + str(totalprice))

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(totalprice),
        "item_name": "Order {}".format(order.id),
        "invoice": str(order.id),
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return": 'http://{}{}'.format(host, reverse('payment:done')),
        "cancel_return": 'http://{}{}'.format(host, reverse('payment:canceled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "order": order}
    return render(request, "process.html", context)
