from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

from swapspace.settings import MEDIA_ROOT
# all items exchange or sell categories, main categories
class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    #slug = models.SlugField(max_length=150, db_index=True, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'catetories'

    def __str__(self):
        return self.name


# all items exchange or sell
class SubCategory(models.Model):
    father_category = models.ForeignKey(Category,
                                        related_name="childCategories",
                                        on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'


class ExchangeItem(models.Model):
    category    = models.ForeignKey(Category,
                                    related_name="items",
                                    on_delete=models.CASCADE)
    user        = models.ForeignKey(User,
                                    related_name="myItems",
                                    on_delete=models.CASCADE)
    name        = models.CharField(max_length=200, db_index=True)

    imagePath   = "exchangeitems/%Y/%m/%d"
    image1      = models.FileField(upload_to=imagePath, default="img/no_img.png")
    # user may not upload more than one images; set default to no_img.png
    image2      = models.FileField(upload_to=imagePath, default="img/no_img.png", null=True, blank=True)
    image3      = models.FileField(upload_to=imagePath, default="img/no_img.png", null=True, blank=True)

    description = models.TextField(validators=[MinLengthValidator(10)])
    status      = models.IntegerField(default=0)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    automatch   = models.ManyToManyField("ExchangeItem",
                                        related_name="myAutoMatcheds",
                                        blank=True)
    request     = models.ManyToManyField("ExchangeItem",
                                        related_name="myRequesteds",
                                        symmetrical=False,
                                        blank=True)
    accept      = models.ManyToManyField("ExchangeItem",
                                        related_name="myAccepteds",
                                        symmetrical=False,
                                        blank=True)
    bestmatch   = models.ForeignKey("ExchangeItem",
                                    related_name="myBestMatch",
                                    on_delete=models.SET_NULL,
                                    blank=True, null=True)
    favorites = models.IntegerField(default=0)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return "{0} posted by {1}".format(self.name, self.user.username)
