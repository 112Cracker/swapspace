from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404
from chat.models import Message
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from .models import ChatRoom, Message
################################################################################
#helper

def isValidRoomname(roomname, chatrooms):
    myrooms = [c.roomname for c in chatrooms]

    for room in myrooms:
        if room == roomname:
            return True
    return False
################################################################################

# Create your views here.
def chat_view(request):
    print("Enter chat/chat_view: entry point to chat room")
    if request.method != "GET":
        raise Http404
        
    return render(request, 'chat-entry.html', {})

@login_required
def chatroom_view(request, roomname):
    print("Enter chat/chatroom._view")
    if request.method != "GET":
        raise Http404

    context = {}
    user = request.user
    
    q1, q2 = Q(user1=user), Q(user2=user)
    chatrooms = ChatRoom.objects.filter(q1 | q2)

    # requested roomname may not exist 
    if not isValidRoomname(roomname, chatrooms):
        print("invalid roomnames")
        context = {'msg': "The room code is invalid for the user."}
        return render(request, 'chat-entry.html', context)

    messages = Message.objects.filter(roomname=roomname)
    return render(request, 'chatroom.html', {
        "messages": messages,
        "roomname": roomname,
        "user": user
    })