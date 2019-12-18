# Generated by Django 2.1.5 on 2019-04-22 21:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'catetories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ExchangeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('image1', models.FileField(default='img/no_img.png', upload_to='exchangeitems/%Y/%m/%d')),
                ('image2', models.FileField(blank=True, default='img/no_img.png', null=True, upload_to='exchangeitems/%Y/%m/%d')),
                ('image3', models.FileField(blank=True, default='img/no_img.png', null=True, upload_to='exchangeitems/%Y/%m/%d')),
                ('description', models.TextField(validators=[django.core.validators.MinLengthValidator(10)])),
                ('status', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('favorites', models.IntegerField(default=0)),
                ('accept', models.ManyToManyField(blank=True, related_name='myAccepteds', to='exchange.ExchangeItem')),
                ('automatch', models.ManyToManyField(blank=True, related_name='myAutoMatcheds', to='exchange.ExchangeItem')),
                ('bestmatch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='myBestMatch', to='exchange.ExchangeItem')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='exchange.Category')),
                ('request', models.ManyToManyField(blank=True, related_name='myRequesteds', to='exchange.ExchangeItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myItems', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150)),
                ('father_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childCategories', to='exchange.Category')),
            ],
            options={
                'verbose_name': 'sub-category',
                'verbose_name_plural': 'sub-categories',
                'ordering': ('name',),
            },
        ),
    ]