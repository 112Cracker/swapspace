from django.urls import path
from django.conf.urls import url
from payment import views

app_name='payment'

urlpatterns = [
    url(r'^process/(?P<order_id>[0-9]+)/$', views.payment_process, name='process'),
    url(r'^done', views.payment_done, name='done'),
    url(r'^canceled', views.payment_canceled, name='canceled'),
]
