from django.contrib.auth.models import User
from django.db import models

from exchange.models import ExchangeItem
from trade.models import SellItem

# Create your models here.

# store user address information
class UserLocation(models.Model):
    user = models.OneToOneField(User,
                             on_delete=models.CASCADE,
                             related_name="myaddress")

    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=5, default="15213")

    class Meta:
        verbose_name = "address"
        ordering = ("state", "city", )


# store user profile information
class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='myprofile')
    activated = models.BooleanField(default=False)

    portraitPath = "portraits/%Y/%m/%d"
    portrait = models.FileField(upload_to=portraitPath, blank=True, null=True)

    bio_text = models.CharField(max_length=500,
                                default="Write Something About Yourself.")

    good = models.IntegerField(default=0)
    fair = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)

    exchangeFavorites = models.ManyToManyField(ExchangeItem, related_name="item_followers", blank=True)
    sellFavorites = models.ManyToManyField(SellItem, related_name="item_followers", blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "profile"
        ordering = ("created", )

    def __str__(self):
        return "%s profile"%(self.user.username)


# store created email information
class EmailRecord(models.Model):
    code = models.CharField(max_length=26)
    email = models.EmailField(max_length=50)

    sendTypes = (
        ('register', 'register'),
        ('forget', 'forget'),
        ('request', 'request')
    )

    sendType = models.CharField(max_length=50, choices=sendTypes)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Email link code"
