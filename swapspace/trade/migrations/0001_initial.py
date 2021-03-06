# Generated by Django 2.1.5 on 2019-04-22 21:18

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exchange', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incart_amount', models.IntegerField(default=0)),
                ('totalprice', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=15)),
                ('buyuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myBuyItems', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_item', models.ManyToManyField(blank=True, to='trade.BuyItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myOrder', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('image1', models.FileField(default='img/no_img.png', upload_to='sellitems/%Y/%d/%d')),
                ('image2', models.FileField(blank=True, default='img/no_img.png', null=True, upload_to='sellitems/%Y/%d/%d')),
                ('image3', models.FileField(blank=True, default='img/no_img.png', null=True, upload_to='sellitems/%Y/%d/%d')),
                ('description', models.TextField(blank=True)),
                ('status', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.IntegerField(default=0)),
                ('favorites', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellitems', to='exchange.Category')),
            ],
        ),
        migrations.AddField(
            model_name='buyitem',
            name='sell_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemsInbuy', to='trade.SellItem'),
        ),
    ]
