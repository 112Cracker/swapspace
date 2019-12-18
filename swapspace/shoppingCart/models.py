from django.db import models
from django.contrib.auth.models import User
from trade.models import SellItem, BuyItem
# Create your models here.


class ShoppingCart(models.Model):
    user = models.OneToOneField(User,
                                related_name='myShoppingCart',
                                on_delete=models.CASCADE)
    buyItem = models.ManyToManyField(BuyItem, blank=True
                                    )
