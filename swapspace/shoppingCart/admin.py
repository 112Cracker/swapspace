from django.contrib import admin
from .models import ShoppingCart
# Register your models here.


class ShoppingCartAdmin(admin.ModelAdmin):
    pass

admin.site.register(ShoppingCart, ShoppingCartAdmin)
