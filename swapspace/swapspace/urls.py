"""swapspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from exchange import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('frontend.urls')),
    path('', views.home, name="home"),
    path('', include('user.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    path('trade/', include('trade.urls')),
    path('exchange/', include('exchange.urls')),
    path('mytrans/', include('mytrans.urls')),
    path('shoppingCart/', include('shoppingCart.urls')),
    path('trade/', include('trade.urls')),
    path('chat/', include("chat.urls")),
    url(r'^payment/', include('payment.urls', namespace="payment")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
