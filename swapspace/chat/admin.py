from django.contrib import admin

from chat.models import Message, ChatRoom
# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    pass

class ChatRoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(Message, MessageAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)