from django.urls import path
from shoppingCart import views

urlpatterns = [
    path('', views.cart_view, name="shoppingCart"),
    path('removeFromCart/<int:id>', views.remove_cart_item, name="remove_cart_item"),
    path('create_order/<int:id>', views.create_order, name="create_order"),
    path('create_bundle_order', views.create_bundle_order, name="create_bundle_order"),
    path('get-shoplist-json', views.get_list_json, name="get_shoplist_json"),
    path('addQuantity', views.addQuantity, name="addQuantity"),
    path('minQuantity', views.minQuantity, name="minQuantity")
]
