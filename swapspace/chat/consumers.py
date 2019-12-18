from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Message

import datetime
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.roomname = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.roomname

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.scope["user"])
        if not self.scope["user"].is_authenticated:
            print("User not logged in.")
            self.close()
        else:
            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("New message received.")

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]
        now = str(datetime.datetime.now()) # .strftime("%m %d, %Y, %H:%M %p")

        if not message or not user.is_authenticated:
            return

        newMessage = Message(user=user,
                             roomname=self.roomname,
                             content=message)
        newMessage.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,
                'now': now,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        now = event['now']
        user = event['user']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now': now,
        }))