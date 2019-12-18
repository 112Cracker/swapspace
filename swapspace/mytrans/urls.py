from django.urls import path
from mytrans import views

urlpatterns = [
    path('', views.allTrans, name="mytrans"),

    # view exchange status 
    path('ongoing', views.ongoing),
    path('finished', views.finished),
    path('cancelled', views.cancelled),

    path('newitem', views.newitem, name="newitem"),
    path('post', views.post_action, name="post"),

    # rate
    path('rate/<int:itemid>', views.rate_action, name="rate"),
    
    # my item
    path('<int:id>', views.item_status, name="status"),
    path('<int:id>/edit', views.edit_item, name="edit"),
    path('<int:id>/cancel', views.cancel_item, name="cancel_item"),
    path('<int:id>/reupload', views.reupload_item, name="reupload"),

    # my item <-> other item
    path('<int:myid>/accept/<int:id>', views.accept_action, name="accept"),
    path('<int:myid>/confirm/<int:id>', views.confirm_action, name="confirm"),
    path('<int:myid>/decline/<int:id>', views.decline_action, name="decline"),
    path('<int:myid>/cancel/<int:id>', views.cancel_action, name="cancel"),

    
]
