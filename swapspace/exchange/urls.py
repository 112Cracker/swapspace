from django.urls import path
from exchange import views
from rest_framework import routers
from .api import CategoryViewSet

# router = routers.DefaultRouter()
# router.register("api/category", CategoryViewSet, 'category')

urlpatterns = [
    path('', views.exchange_view, name="exchange"),
    path('items/<int:id>', views.item_detail_view, name="item_detail"),
    path('request/<ids>', views.request_item_view, name="request"),
    path('<int:ordering>', views.order_exchange_view),
    path('<category>', views.category_view),
    path('<category>/<int:ordering>', views.order_category_view),
]

# urlpatterns += router.urls