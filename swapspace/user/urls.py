from django.urls import path
from user import views


urlpatterns = [
    # user basic urls
    path("login", views.login_action, name="login"),
    path("logout", views.logout_action, name="logout"),
    path("register", views.register_action, name="register"),

    # profile related urls
    path("myprofile", views.view_profile_action, name="myprofile"),
    path("edit-profile", views.edit_profile_action, name="edit-profile"),
    path("picture/<username>", views.get_picture_action, name='profile_picture'),

    # address related urls
    path("myaddress", views.view_address_action, name="myaddress"),
    path("create-address", views.create_address_action, name="create-address"),
    path("edit-address", views.edit_address_action, name="edit-address"),

    # pwd related urls
    path("activate/<code>", views.activate_action, name="activate"),
    path("reset/<code>", views.get_reset_action, name="reset"),
    path("update/", views.update_pwd_action, name="update-pwd"),
    path("forget/", views.forget_pwd_action, name="forget"),

    # add to favorite
    path("favorite", views.favorite_action),
    path("favorite-sell", views.favorite_sell_action),
    path("myitems/<int:itemId>", views.get_myitems),

    path("search/<keywords>", views.search_action)
]