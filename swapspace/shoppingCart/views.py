from django.shortcuts import render
from django.http import HttpResponse, Http404
from trade.models import Category, SellItem, BuyItem
from django.contrib.auth.decorators import login_required
from .models import ShoppingCart
from trade.models import Order
from django.core import serializers
import json
from decimal import Decimal
from user.models import UserLocation

def getCartNum(request):
    user = request.user
    cartNum = 0
    if user.is_authenticated:
        cartNum = ShoppingCart.objects.get(user=user).buyItem.count()
    return cartNum
    
# Create your views here.
def home(request):
    categories = Category.objects.all()
    context = {"categories": categories}

    return render(request, 'index.html', context)

@login_required
def cart_view(request):
    if request.method != "GET":
        raise Http404
    cart = ShoppingCart.objects.get(user=request.user)
    items = cart.buyItem.all()
    totalprice = 0.00
    for item in items:
        totalprice += float(item.sell_item.price)
    cartNum = getCartNum(request)
    context = {"items": items, "totalprice":str(totalprice), "cartNum": cartNum}
    return render(request, 'cart.html', context)

@login_required
def remove_cart_item(request, id):
    if request.method != "GET":
        raise Http404
    cart = ShoppingCart.objects.get(user=request.user)
    item = BuyItem.objects.get(pk=id)
    cart.buyItem.remove(item)
    items = cart.buyItem.all()
    totalprice = 0.00
    for i in items:
        totalprice += float(i.sell_item.price)
    cartNum = getCartNum(request)
    context = {"items":items, "totalprice":str(totalprice), "cartNum": cartNum}
    print(items)
    return render(request, 'cart.html', context)

# the checkout button in the shopping cart page for each
# item after clicking create order in models
# then go to create_order page to fill buyer info
def create_order(request, id):
    cart = ShoppingCart.objects.get(user=request.user)
    item = SellItem.objects.get(pk=id)
    #create new order for this item
    # use sell_item.price to present the total price for order
    new_order = Order(user=request.user,
                    sell_item=item)
    new_order.save()
    #remove the item from the shopping cart
    cart.sellItem.remove(item)
    cartNum = getCartNum(request)
    return render(request, 'create_order.html',{"order":new_order, "cartNum": cartNum})

def create_bundle_order(request):
    cart = ShoppingCart.objects.get(user=request.user)
    items = cart.buyItem.all()
    new_order = Order(user=request.user)
    new_order.save()
    totalprice = 0.00
    for item in items:
        new_order.buy_item.add(item)
        totalprice += float(item.totalprice)
    if UserLocation.objects.filter(user=request.user):
        address = UserLocation.objects.filter(user=request.user)[0]
    else:
        address = []
    cartNum = getCartNum(request)
    return render(request, 'create_order.html', {"order":new_order,
                                                 "items":items,
                                                 "totalprice":str(totalprice),
                                                 "address":address,
                                                 "cartNum":cartNum})


def get_list_json(request):
    cart = ShoppingCart.objects.filter(user=request.user)[0]
    response_sells = serializers.serialize('json', cart.buyItem.all())
    data = {'change':response_sells}
    return HttpResponse(json.dumps(data), content_type='application/json')

def addQuantity(request):
    if request.method != 'POST':
        raise Http404
    if not 'current_buy_item_id' in request.POST:
        response_quantity = serializers.serialize('json', [])
    else:
        current_buy_item_id = request.POST['current_buy_item_id']
        buyItem = BuyItem.objects.filter(id=current_buy_item_id)[0]
        if buyItem.incart_amount < buyItem.sell_item.amount:
            buyItem.incart_amount += 1
        buyItem.totalprice = Decimal(buyItem.incart_amount * float(buyItem.sell_item.price))
        buyItem.save()
    cart = ShoppingCart.objects.filter(user=request.user)[0]
    response_sells = serializers.serialize('json', cart.buyItem.all())
    data = {'change':response_sells}
    return HttpResponse(json.dumps(data), content_type='application/json')


def minQuantity(request):
    if request.method != 'POST':
        raise Http404
    if not 'current_buy_item_id' in request.POST:
        response_quantity = serializers.serialize('json', [])
    else:
        current_buy_item_id = request.POST['current_buy_item_id']
        buyItem = BuyItem.objects.filter(id=current_buy_item_id)[0]
        if buyItem.incart_amount > 0:
            buyItem.incart_amount -= 1
        buyItem.totalprice = Decimal(buyItem.incart_amount * float(buyItem.sell_item.price))
        buyItem.save()
    cart = ShoppingCart.objects.filter(user=request.user)[0]
    response_sells = serializers.serialize('json', cart.buyItem.all())
    data = {'change':response_sells}
    return HttpResponse(json.dumps(data), content_type='application/json')
