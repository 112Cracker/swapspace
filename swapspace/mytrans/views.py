from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from user.models import UserProfile
from exchange.models import Category, ExchangeItem
from mytrans.forms import ExchangeItemForm
from utils.sendEmail import sendEmail

HOST = "http://74739114.ngrok.io"

@login_required
def allTrans(request):
    user = request.user

    context = {}
    context['items'] = ExchangeItem.objects.filter(user=user).order_by('-updated')
    context['checkstatus'] = 0

    return render(request, 'mytrans.html', context)


@login_required
def ongoing(request):
    user = request.user

    context = {}
    context['items'] = ExchangeItem.objects.filter(user=user).filter(status__lte=2).order_by('-updated')
    context['checkstatus'] = 1

    return render(request, 'mytrans.html', context)


@login_required
def finished(request):
    user = request.user

    context = {}
    context['items'] = ExchangeItem.objects.filter(user=user).filter(status__gte=3).filter(status__lte=4).order_by('-updated')
    context['checkstatus'] = 2

    return render(request, 'mytrans.html', context)


@login_required
def cancelled(request):
    user = request.user

    context = {}
    context['items'] = ExchangeItem.objects.filter(user=user).filter(status=5).order_by('-updated')
    context['checkstatus'] = 3

    return render(request, 'mytrans.html', context)


@login_required
def newitem(request):
    context = {}
    context['form'] = ExchangeItemForm()
    return render(request, 'new-item.html', context)


@login_required
def post_action(request):
    # GET
    if request.method == 'GET':
        return HttpResponseRedirect('')

    # POST
    context = {}
    new_item = ExchangeItem(user=request.user)
    form = ExchangeItemForm(request.POST, request.FILES, instance=new_item)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'new-item.html', context)

    # Save the new record
    form.save()
    print("New item posted!")
    return HttpResponseRedirect('ongoing')


@login_required
def rate_action(request, itemid):
    completed_item = ExchangeItem.objects.get(pk=itemid)
    bestmatch = completed_item.bestmatch
    match_owner = bestmatch.user

    if request.method == "GET":
        context = {
            'itemid': itemid,
            'match_owner': match_owner
        }
        return render(request, "rate.html", context)

    if "rating" not in request.POST:
        raise Http404
    rating = request.POST.get("rating")
    

    match_user_profile = UserProfile.objects.get(user=match_owner)

    if rating == "good":
        match_user_profile.good += 1
    elif rating == "bad":
        match_user_profile.bad += 1
    elif rating == "fair":
        match_user_profile.fair += 1
    else:
        raise Http404

    match_user_profile.save()
    completed_item.status = 4
    completed_item.save()

    return redirect(reverse("mytrans"))


@login_required
def item_status(request, id):
    print("Enter mytrans/item_status")
    user = request.user
    item = get_object_or_404(ExchangeItem, id=id)

    # protect page from invalid visit
    # user cannot view other user item status
    # user cannot view completed item status
    if user != item.user or item.status == 4:
        raise Http404

    if item.status == 3:
        return redirect(reverse('rate', kwargs={"itemid": id}))

    address = "No address set"
    try:
        owner_address = item.user.myaddress
        address = owner_address.address1 + ", " + owner_address.city + ", " + owner_address.state + ", " + owner_address.zip_code
    except ObjectDoesNotExist:
        pass

    context = {"item": item,
               "address": address}
    return render(request, 'item-status.html', context)


@login_required
def edit_item(request, id):
    print("Enter edit_item")

    # GET: view user profile
    if request.method == "GET":
        context = {}
        context['form'] = ExchangeItemForm(instance=ExchangeItem.objects.get(pk=id))
        context['item'] = ExchangeItem.objects.get(pk=id)
        return render(request, "edit-item.html", context)

    # POST: update user profile
    item = ExchangeItem.objects.select_for_update().get(pk=id)

    if request.FILES:
        print("User upload new picture.")
        form = ExchangeItemForm(request.POST, request.FILES, instance=item)
    else:
        print("User upload nothing.")
        form = ExchangeItemForm(request.POST, instance=item)

    context = {}
    if not form.is_valid():
        context['form'] = form
        context['item'] = item
        return render(request, 'edit-item.html', context)

    # Save the new record
    item.update_time = timezone.now()
    form.save()

    return redirect(reverse('status', kwargs={'id': id}))

@login_required
def cancel_item(request, id):
    print("Enter cancel_item")
    if request.method != "GET":
        raise Http404

    item = ExchangeItem.objects.get(pk=id)

    # update item status
    item.status = 5
    item.bestmatch = None
    item.save()

    # clean up exchange logic list
    item.request.clear()
    item.myRequesteds.clear()
    item.accept.clear()
    item.myAccepteds.clear()
    item.automatch.clear()
    item.myAutoMatcheds.clear()

    return redirect(reverse('status', kwargs={'id': id}))


@login_required
def reupload_item(request, id):
    print("Enter reupload_item")
    if request.method != "GET":
        raise Http404

    item = ExchangeItem.objects.get(pk=id)
    # update item status
    item.status = 0
    item.save()

    return redirect(reverse('status', kwargs={'id': id}))


@login_required
def accept_action(request, myid, id):
    print("Enter accept_action")
    if request.method != "GET":
        raise Http404

    user = request.user
    userEmail = user.email
    myitem = ExchangeItem.objects.get(pk=myid)

    item = ExchangeItem.objects.get(pk=id)
    owner = item.user
    ownerEmail = owner.email
    msg = """Hi {0},\n\n
             Your exchange for "{1}" with your "{2}" has been accepted.\n
             Come back to {5} to confirm the exchange if you hasn't change your mind!\n
             You can contact "{1}"'s owner {3} through SwapSpace's chat room or at {4}. Thanks!"""\
             .format(owner, myitem.name, item.name, user, userEmail, HOST)
    sendEmail(ownerEmail, "accept", msg)

    # update item status
    if myitem.status < 2:
        myitem.status = 2
        myitem.bestmatch = item
        myitem.save()
    if item.status < 2:
        item.status = 2
        item.bestmatch = myitem
        item.save()

    # update exchange logic list
    item.request.remove(myitem)
    myitem.accept.add(item)

    return redirect(reverse('status', kwargs={'id': myid}))


@login_required
def confirm_action(request, myid, id):
    print("Enter confirm_action")
    if request.method != "GET":
        raise Http404

    user = request.user
    userEmail = user.email
    myitem = ExchangeItem.objects.get(pk=myid)

    item = ExchangeItem.objects.get(pk=id)
    owner = item.user
    ownerEmail = owner.email
    msg = """Hi {0},\n\n
             Your exchange for "{2}" with your "{1}" has been confirmed.\n
             Remember to rate this exchange at {5}:/rate/{6}!\n
             You can contact "{2}"'s owner {3} at {4}. Thanks!"""\
             .format(owner, item.name, myitem.name,
                     user, userEmail, HOST, id)

    sendEmail(ownerEmail, "confirm", msg)

    # update item status
    myitem.status = 3
    myitem.bestmatch = item
    myitem.save()
    item.status = 3
    item.bestmatch = myitem
    item.save()

    # clean up exchange logic list
    myitem.request.clear()
    myitem.myRequesteds.clear()
    myitem.accept.clear()
    myitem.myAccepteds.clear()
    myitem.automatch.clear()
    myitem.myAutoMatcheds.clear()
    item.request.clear()
    item.myRequesteds.clear()
    item.accept.clear()
    item.myAccepteds.clear()
    item.automatch.clear()
    item.myAutoMatcheds.clear()

    return redirect(reverse('status', kwargs={'id': myid}))


@login_required
def decline_action(request, myid, id):
    print("Enter decline_action")
    if request.method != "GET":
        raise Http404

    myitem = ExchangeItem.objects.get(pk=myid)
    item = ExchangeItem.objects.get(pk=id)

    # update exchange logic list
    item.request.remove(myitem)

    return redirect(reverse('status', kwargs={'id': myid}))


@login_required
def cancel_action(request, myid, id):
    print("Enter cancel_action")
    if request.method != "GET":
        raise Http404

    user = request.user
    myitem = ExchangeItem.objects.get(pk=myid)

    item = ExchangeItem.objects.get(pk=id)
    owner = item.user
    ownerEmail = owner.email
    msg = """Hi {0},\n\n
             Your exchange for "{1}" with your "{2}" has been cancelled by user {3}.\n
             Come back to check for more exchange options!""".format(owner, myitem.name, item.name, user)
    sendEmail(ownerEmail, "cancel", msg)

    # update exchange logic list
    if myitem in item.request.all():
        item.request.remove(myitem)
    elif item in myitem.request.all():
        myitem.request.remove(item)
    elif myitem in item.accept.all():
        item.accept.remove(myitem)
    elif item in myitem.accept.all():
        myitem.accept.remove(item)

    return redirect(reverse('status', kwargs={'id': myid}))
