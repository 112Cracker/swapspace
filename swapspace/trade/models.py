from django.db import models
from django.contrib.auth.models import User
# from shoppingCart.models import ShoppingCart
from exchange.models import Category
from decimal import Decimal
# Create your models here.



class SellItem(models.Model):
    category    = models.ForeignKey(Category,
                                related_name="sellitems",
                                on_delete=models.CASCADE)

    # sell items are posted by the website
    # user = models.ForeignKey(User,
    #                          related_name='mySellItems',
    #                          on_delete=models.CASCADE)
    # maybe not necessary
    # user = models.ForeignKey(User,
    #                         related_name='mySellItems',
    #                         on_delete=models.CASCADE)
    ## maybe manytomany
    name        = models.CharField(max_length=200, db_index=True)
    imagePath   = "sellitems/%Y/%d/%d"
    image1      = models.FileField(upload_to=imagePath, default="img/no_img.png")
    image2      = models.FileField(upload_to=imagePath, default="img/no_img.png", null=True, blank=True)
    image3      = models.FileField(upload_to=imagePath, default="img/no_img.png", null=True, blank=True)

    description = models.TextField(blank=True)
    status      = models.IntegerField(default=0)   # the transaction state 0: not paid 1: paid
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(default=0)

    favorites = models.IntegerField(default=0)
    # created     = models.DateTimeField(auto_now_add=True)
    # updated     = models.DateTimeField(auto_now=True)
    # sell items are posted by the website
    # location = models.CharField(max_length=200)

    def __str__(self):
        return "sell item: {0}".format(self.name)

class BuyItem(models.Model):
    buyuser = models.ForeignKey(User,
                                related_name='myBuyItems',
                                on_delete=models.CASCADE,
                                )
    incart_amount = models.IntegerField(default=0)
    sell_item = models.ForeignKey(SellItem,
                                    related_name="itemsInbuy",
                                    on_delete=models.CASCADE)
    totalprice = models.DecimalField(max_digits=15, decimal_places=2,default=Decimal(0))
    def subtotal(self):
        return self.incart_amount*self.sell_item.price


class Order(models.Model):
    user = models.ForeignKey(User,
                            related_name="myOrder",
                            on_delete=models.CASCADE)
    #tend to be foreignkey in the SellItem model
    buy_item = models.ManyToManyField(BuyItem,
                                    blank=True)
