from django.urls import path
from trade import views

urlpatterns = [
    path('', views.sell_view, name="trade"),
    path('viewAddToCart/<int:id>', views.itempage_addtocart),
    path('addToCart/<int:id>', views.addToCart, name="addToCart"),
    path('mycart', views.view_mycart, name="mycart"),
    path('<int:ordering>', views.order_sell_view),
    path('<category>', views.category_view),
    path('items/<int:id>', views.item_detail_view),
    path('search/<keywords>', views.search_action),
    path('<category>/<int:ordering>', views.order_category_view)
]
