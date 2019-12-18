from __future__ import absolute_import, unicode_literals

from celery import shared_task, task
from .models import Category, ExchangeItem

import math

@shared_task(name='automatch')
def automatch():
    print("Enter exchange/tasks.automatch")
    match_set = ExchangeItem.objects.filter(status__lte=2)
    owner_grades = {}
    for item in match_set:
        owner_profile = item.user.myprofile
        owner_grades[item.id] = 4.0
        if owner_profile.good != 0 or owner_profile.fair != 0 or owner_profile.bad != 0:
            rate_cnt = owner_profile.good + owner_profile.fair + owner_profile.bad
            score = (owner_profile.good * 5 + owner_profile.fair * 3.5 + owner_profile.bad * 1) / rate_cnt
            owner_grades[item.id] = round(score, 2)

    for item1 in match_set:
        item1.automatch.clear()
        match_grades = {}
        for item2 in match_set:
            if item1.user == item2.user:
                continue
            match_grade = round(math.sqrt(abs(item1.price - item2.price)/item1.price * 100), 2) + (5-owner_grades[item2.id]) * 5.0
            #print(" match_grade between " + item1.name + " and " + item2.name + "is: " + str(match_grade))
            if match_grade < 30:
                match_grades[item2.id] = match_grade
            grades = sorted(match_grades.values())
            if len(match_grades) > 3:
                for k,v in match_grades.items():
                    if v == grades[3]:
                        del match_grades[k]
                        break

        if len(match_grades) == 0:
            continue;

        match_ids, tmp = zip(*sorted(match_grades.items(), key=lambda t: t[1]))
        if len(match_ids) >= 1:
            item1.automatch.add(ExchangeItem.objects.get(id=match_ids[0]))
            if item1.status <= 1:
                ExchangeItem.objects.filter(id=item1.id).update(bestmatch=ExchangeItem.objects.get(id=match_ids[0]))
        if len(match_ids) >= 2:
            item1.automatch.add(ExchangeItem.objects.get(id=match_ids[1]))
        if len(match_ids) == 3:
            item1.automatch.add(ExchangeItem.objects.get(id=match_ids[2]))

    return

@shared_task(name='updatestatus')
def updatestatus():
    print("Enter exchange/tasks.updatestatus")
    # check item at single-side request status
    for item in ExchangeItem.objects.filter(status=1):
        if item.request.all().count() == 0 and item.myRequesteds.all().count() == 0:
            item.status = 0
            item.save()

    # check item at request accepted status
    for item in ExchangeItem.objects.filter(status=2):
        if item.accept.all().count() == 0 and item.myAccepteds.all().count() == 0:
            item.status = 1
            if item.request.count() == 0 and item.myRequesteds.count() == 0:
                item.status = 0
            item.save()


# def sendrequest(ids):
#     ids = ids.split()
#     myItemId, itemId, roomname = int(ids[0]), int(ids[1]), int(ids[2])

#     # check if the ids are valid
#     if ExchangeItem.objects.filter(pk=myItemId).count() == 0 or \
#        ExchangeItem.objects.filter(pk=myItemId).count() ==0:
#        raise Http404


#     myItem = ExchangeItem.objects.get(pk=myItemId)
#     user = request.user
#     userEmail = user.email

#     otherItem = ExchangeItem.objects.get(pk=itemId)
#     owner = otherItem.user
#     ownerEmail = owner.email

#     context = {"name": otherItem.name,
#                "id": otherItem.pk,
#                "description": otherItem.description,
#                "price": otherItem.price,
#                "status": otherItem.status,
#                "item": otherItem,
#                "owner": otherItem.user}

#     print(userEmail, ownerEmail)
#     msg1 = """Hi {0},\n\n
#              User {1} would like to exchange for your "{2}" with "{3}".\n
#              Accept this request if you are interested!\n
#              You can contact {1} through:\n
#              1. SwapSpace's chatroom at http://74739114.ngrok.io/chat, enter code <{5}> to start chatting!\n
#              2. Or at {4}. Thanks!""".format(owner, user, otherItem, myItem, userEmail, roomname)
#     sendEmail(ownerEmail, "request", msg1)

#     msg2 = """Hi {0},\n\n
#              Your exchange request for "{1}" with your "{2}" has been sent successfully!\n
#              To follow up this request, \n
#              1. SwapSpace's chatroom at http://74739114.ngrok.io/chat, enter code <{4}> to start chatting!\n
#              2. Or at {3}. Thanks!""".format(user, otherItem, myItem, ownerEmail, roomname)
#     sendEmail(userEmail, "request", msg2)
