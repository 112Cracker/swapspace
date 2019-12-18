from django.contrib import admin

# Register your models here.
from .models import SellItem, Order, BuyItem


class SellItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(SellItem, SellItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)

class BuyItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(BuyItem, BuyItemAdmin)
