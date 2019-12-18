from django.urls import path
# from django.conf.urls import url

from chat import views

# urlpatterns = [
#     url(r'^$', views.chat_view, name='index'),
#     url(r'^(?P<roomname>[^/]+)/$', views.chatroom_view, name='room'),
# ]
urlpatterns = [
    path('', views.chat_view, name="chat"),
    path('<str:roomname>/', views.chatroom_view, name="chatroom"),
]