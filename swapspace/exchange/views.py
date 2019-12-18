from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Category, ExchangeItem
from chat.models import ChatRoom, Message
from shoppingCart.models import ShoppingCart

from utils.sendEmail import sendEmail, generateRandomCode
# from .tasks import sendrequest
################################################################################
# helper function

# load user, all categories
# and items not owned by the login user and status <= 1
def loadUserCategoriesItems(request):
    user = request.user
    categories = Category.objects.all()

    if user.is_authenticated:
        print("User is authenticated!")
        user = request.user
    items = ExchangeItem.objects
    if user.is_authenticated:
        items = ExchangeItem.objects.exclude(user=user)
    items = items.filter(status__lte=1)
    return (user, categories, items)

def calcRates(owner_profile):
    if owner_profile.good != 0 or owner_profile.fair != 0 or owner_profile.bad != 0:
        rate_cnt = owner_profile.good + owner_profile.fair + owner_profile.bad
        score = (owner_profile.good * 5 + owner_profile.fair * 3.5 + owner_profile.bad * 1) / rate_cnt
        rating = [1] * round(score)
    else:
        rate_cnt, score, rating = 0, 0, []
    return rate_cnt, score, rating

ROOMNAME_LENGTH = 21
#################################################################################
# Create your views here.
def home(request):
    # do not support POST
    print("Enter exchange/home view")
    if request.method !="GET":
        raise Http404

    user, categories, items = loadUserCategoriesItems(request)
    items = items.order_by('-updated')[:3]# dummy recommand by return top 3 recent updated

    context = {"categories": categories, "items": items, "user": user}

    return render(request, 'index.html', context)

# view all exchange items
def exchange_view(request):
    # do not support POST
    print("Enter exchange/exchange view")
    if request.method != "GET":
        raise Http404

    user, categories, items = loadUserCategoriesItems(request)

    context = {"items": items, "categories": categories, "user": user}
    return render(request, 'exchange.html', context)


# view all exchange items in order: ordering
# 0: topRated; 1: mostRecent; 2:lowToHigh; 3: highToLow
def order_exchange_view(request, ordering=0):
    print("Enter exchange/order_exchange_view: view all exchange items in order.")
    # do not support POST
    if request.method != "GET":
        raise Http404

    user, categories, items = loadUserCategoriesItems(request)

    if ordering == 0:
        pass
    elif ordering == 1:
        items = items.order_by('-updated')
    elif ordering == 2:
        items = items.order_by("price")  # ascending order by price
    elif ordering == 3:
        items = items.order_by("-price") # descending order by price

    context = {"items": items,
               "categories": categories,
               "ordering": ordering}
    return render(request, 'exchange.html', context)


# view items of a given category
def category_view(request, category):
    print("Enter exchange/category_view: view items by category.")
    if request.method != "GET":
        raise Http404

    user, categories, items = loadUserCategoriesItems(request)

    category = Category.objects.get(name=category)
    items = items.filter(category=category)

    context = {"items": items,  # items of category
               "category": category, # given category
               "categories": categories}
    return render(request, 'exchange.html', context)

# view items of a given category in order: ordering
# 0: topRated; 1: mostRecent; 2:lowToHigh; 3: highToLow
def order_category_view(request, category, ordering=0):
    print("Enter order_category_view: view items by category in order.")
    if request.method != "GET":
        raise Http404

    user, categories, items = loadUserCategoriesItems(request)

    category = Category.objects.get(name=category)
    items = items.filter(category=category)

    if ordering == 0:
        pass
    elif ordering == 1:
        items = items.order_by('-updated')
    elif ordering == 2:
        items = items.order_by("price")
    elif ordering == 3:
        items = items.order_by("-price")

    context = {"items": items,
               "category": category, # given category
               "categories": categories,
               "ordering": ordering, # given ordering
               "user": user}
    return render(request, 'exchange.html', context)


# view item details
# item status 
# 0: no response; 1: single-side request; 2: in exchange; 3: complete exchange; 4: cancel exchange
@login_required
def item_detail_view(request, id):
    print("Enter exchange/item_detail_view")
    if request.method != "GET":
        raise Http404
        
    user = request.user
    item = ExchangeItem.objects.get(pk=id)

    # protect page from invalid visit
    if user == item.user and item.status <= 2:
        raise Http404

    owner_profile = item.user.myprofile
    rating = [1] * 4
    rate_cnt, score, rating = calcRates(owner_profile)

    address = "No address set"
    try:
        owner_address = item.user.myaddress
        address = owner_address.address1 + ", " + owner_address.city + ", " + owner_address.state + ", " + owner_address.zip_code
    except ObjectDoesNotExist:
        pass

    # derive exchange condition between user and this item
    exchange_condition = -1
    if item.status == 0:
        exchange_condition = 0
    elif item.status == 1:
        for req in item.myRequesteds.all():
            if req.user == user:
                exchange_condition = 1.0
                break
        if exchange_condition == -1:
            for req in item.request.all():
                if req.user == user:
                    exchange_condition = 1.1
                    break
        if exchange_condition == -1:
            exchange_condition = 1.2
    elif item.status == 2:
        for req in item.myRequesteds.all():
            if req.user == user:
                exchange_condition = 2.0
                break
        if exchange_condition == -1:
            for req in item.request.all():
                if req.user == user:
                    exchange_condition = 2.1
                    break
        if exchange_condition == -1:
            for req in item.myAccepteds.all():
                if req.user == user:
                    exchange_condition = 2.2
                    break
        if exchange_condition == -1:
            for req in item.accept.all():
                if req.user == user:
                    exchange_condition = 2.3
                    break
        if exchange_condition == -1:
            exchange_condition = 2.4
    print(exchange_condition)

    if item in user.myprofile.exchangeFavorites.all():
        rated = True
    else:
        rated = False

    context = {"owner": item.user,
               "profile": owner_profile,
               "rating": rating,
               "range": "1"*(5-len(rating)),
               "rate_cnt": rate_cnt,
               "item": item,
               "address": address,
               "exchange_condition": exchange_condition,
               "rated": rated}

    return render(request, 'item-detail.html', context)


# send a request to a item
@login_required
def request_item_view(request, ids):
    print("Enter exchange/request_item_view")
    if request.method != "GET":
        raise Http404
    ids = ids.split(" ")

    # double check the url data
    if len(ids) != 2 or not ids[0].isnumeric() or not ids[1].isnumeric():
        raise Http404

    myItemId, itemId = int(ids[0]), int(ids[1])

    # check if the ids are valid
    if ExchangeItem.objects.filter(pk=myItemId).count() == 0 or \
       ExchangeItem.objects.filter(pk=myItemId).count() ==0:
       raise Http404

    # ids.append(roomname)
    # sendrequest.delay(" ".join(ids))

    myItem = ExchangeItem.objects.get(pk=myItemId)
    user = request.user
    userEmail = user.email

    otherItem = ExchangeItem.objects.get(pk=itemId)
    owner = otherItem.user
    ownerEmail = owner.email

    roomname = generateRandomCode(ROOMNAME_LENGTH)
    chatroom = ChatRoom(user1=user, user2=owner, roomname=roomname)
    chatroom.save()

    # update both item status
    myItem.request.add(otherItem)
    if myItem.status < 1:
        myItem.status = 1
    if otherItem.status < 1:
        otherItem.status = 1
    myItem.save()
    otherItem.save()

    context = {"name": otherItem.name,
               "id": otherItem.pk,
               "description": otherItem.description,
               "price": otherItem.price,
               "status": otherItem.status,
               "item": otherItem,
               "owner": otherItem.user}
    # master
    # context = {"name": otherItem.name,
    #            "id": otherItem.pk,
    #            "description": otherItem.description,
    #            "price": otherItem.price,
    #            "status": otherItem.status,
    #            "owner": otherItem.user,
    #            "item": otherItem,
    #            "myItem": myItem}
    #            master

    print(userEmail, ownerEmail)
    msg1 = """Hi {0},\n\n
             User {1} would like to exchange for your "{2}" with "{3}".\n
             Accept this request if you are interested!\n
             You can contact {1} through:\n
             1. SwapSpace's chatroom at http://74739114.ngrok.io/chat, enter code <{5}> to start chatting!\n
             2. Or at {4}. Thanks!""".format(owner, user, otherItem, myItem, userEmail, roomname)
    sendEmail(ownerEmail, "request", msg1)

    msg2 = """Hi {0},\n\n
             Your exchange request for "{1}" with your "{2}" has been sent successfully!\n
             To follow up this request, \n
             1. SwapSpace's chatroom at http://74739114.ngrok.io/chat, enter code <{4}> to start chatting!\n
             2. Or at {3}. Thanks!""".format(user, otherItem, myItem, ownerEmail, roomname)
    sendEmail(userEmail, "request", msg2)

    return redirect(reverse('item_detail', kwargs={'id': otherItem.pk}))
    #return HttpResponseRedirect(reverse('item_detail', kwargs={'id': itemId}))
