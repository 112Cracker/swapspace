from django.contrib import admin
from .models import Category, ExchangeItem

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(ExchangeItem, ItemAdmin)