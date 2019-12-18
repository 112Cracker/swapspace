from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse

from .models import SellItem, BuyItem
from exchange.models import Category
from shoppingCart.views import cart_view
from shoppingCart.models import ShoppingCart
from django.urls import reverse
from django.core import serializers
import re, json
# Create your views here.

def getCartNum(request):
    user = request.user
    cartNum = 0
    if user.is_authenticated:
        cartNum = ShoppingCart.objects.get(user=user).buyItem.count()
    return cartNum

# Create your views here.
def sell_view(request):
    if request.method != "GET":
        raise Http404

    categories = Category.objects.all()
    items = SellItem.objects.all()
    cartNum = getCartNum(request)

    context = {"items": items, "categories": categories, "cartNum": cartNum, "is_trade": True}
    return render(request, 'sellPage.html', context)


def order_sell_view(request, ordering=0):
    print("Enter order_exchange_view: view all exchange items in order.")
    if request.method != "GET":
        raise Http404

    items = SellItem.objects.all()
    categories = Category.objects.all()
    if ordering == 0:
        pass
    elif ordering == 1:
        pass
    elif ordering == 2:
        items = items.order_by("price")
    elif ordering == 3:
        items = items.order_by("-price")

    user = None
    if request.user.is_authenticated:
        print("User is authenticated!")
        user = request.user
    cartNum = getCartNum(request)
    context = {"items": items,
               "categories": categories,
               "ordering": ordering,
               "user": user,
               "cartNum": cartNum,
               "is_trade": True}

    return render(request, 'sellPage.html', context)


def category_view(request, category):
    print("Enter category_view: view items by category.")
    if request.method != "GET":
        raise Http404

    categories = Category.objects.all()
    category = Category.objects.get(name=category)
    items = SellItem.objects.filter(category=category)

    user = None
    if request.user.is_authenticated:
        print("User is authenticated!")
        user = request.user
    cartNum = getCartNum(request)
    context = {"items": items,
               "category": category,
               "categories": categories,
               "user": user,
               "cartNum": cartNum,
               "is_trade": True}
    return render(request, 'sellPage.html', context)

def search_action(request, keywords):
    print("Enter user/search_action")
    words = re.findall(r"[\w']+", keywords)
    print(keywords)

    res_items = set()
    for w in words:
        items = SellItem.objects.filter(description__icontains=w)
        print("number is " + str(items.count()))
        for i in items:
            res_items.add(i)

    res_items = serializers.serialize('json', res_items)
    data = {"items": res_items}
    return HttpResponse(json.dumps(data), content_type='application/json')

def order_category_view(request, category, ordering=0):
    print("Enter order_category_view: view items by category in order.")
    if request.method != "GET":
        raise Http404

    category = Category.objects.get(name=category)
    items = SellItem.objects.filter(category=category)

    categories = Category.objects.all()
    if ordering == 0:
        pass
    elif ordering == 1:
        pass
    elif ordering == 2:
        items = items.order_by("price")
    elif ordering == 3:
        items = items.order_by("-price")

    user = None
    if request.user.is_authenticated:
        print("User is authenticated!")
        user = request.user
    cartNum = getCartNum(request)
    context = {"items": items,
               "category": category,
               "categories": categories,
               "ordering": ordering,
               "user": user,
               "cartNum": cartNum,
               "is_trade": True}
    return render(request, 'sellPage.html', context)


@login_required
def view_mycart(request):
    if request.method != "GET":
        raise Http404

    user = request.user
    cart = ShoppingCart.objects.filter(user=request.user).first()
    items = cart.buyItem.all()

    totalprice = 0.00
    for item in items:
        totalprice += float(item.sell_item.price)

    cartNum = getCartNum(request)
    context = {
        "user": user,
        "cart": cart,
        "items": items,
        "totalprice": totalprice,
        "cartNum": cartNum,
        "is_trade": True
    }
    return render(request, "cart.html", context)

@login_required
def addToCart(request, id):
    if request.method != "GET":
        raise Http404

    # POST request
    user = request.user

    if not request.user.is_authenticated:
        return reirect(reverse('login'))

    print("User is authenticated!")
    cart = ShoppingCart.objects.filter(user=request.user).first()
    item = SellItem.objects.get(pk=id)
    buyItem = BuyItem(buyuser=request.user,
                        sell_item=item,
                        incart_amount=1,
                        totalprice=item.price)
    buyItem.save()
    cart.buyItem.add(buyItem)
    cart.save()

    categories = Category.objects.all()
    items = SellItem.objects.all()
    cartNum = getCartNum(request)
    context = {"items": items, "categories": categories, "cartNum": cartNum, "is_trade": True}
    print("Add to cart success")
    return render(request, 'sellPage.html', context)

@login_required
def item_detail_view(request, id):
    print("Enter item_detail_view")
    if request.method != "GET":
        raise Http404

    user = request.user

    item = SellItem.objects.get(pk=id)

    if item in user.myprofile.sellFavorites.all():
        rated = True
    else:
        rated = False
    cartNum = getCartNum(request)
    context = {"item": item, "rated": rated, "cartNum": cartNum, "is_trade": True}

    return render(request, 'sell-item-detail.html', context)

@login_required
def itempage_addtocart(request, id):
    cart = ShoppingCart.objects.filter(user=request.user).first()
    item = SellItem.objects.get(pk=id)
    buyItem = BuyItem(buyuser=request.user,
                        sell_item=item,
                        incart_amount=1,
                        totalprice=item.price)
    buyItem.save()
    cart.buyItem.add(buyItem)
    cart.save()
    cartNum = getCartNum(request)
    return render(request, 'sell-item-detail.html', {"item": item, "cartNum": cartNum, "is_trade": True})
