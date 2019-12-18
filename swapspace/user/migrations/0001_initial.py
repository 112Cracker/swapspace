# Generated by Django 2.1.5 on 2019-04-22 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trade', '0001_initial'),
        ('exchange', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=26)),
                ('email', models.EmailField(max_length=50)),
                ('sendType', models.CharField(choices=[('register', 'register'), ('forget', 'forget'), ('request', 'request')], max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Email link code',
            },
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=150)),
                ('address2', models.CharField(blank=True, max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('zip_code', models.CharField(default='15213', max_length=5)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='myaddress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'address',
                'ordering': ('state', 'city'),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activated', models.BooleanField(default=False)),
                ('portrait', models.FileField(blank=True, null=True, upload_to='portraits/%Y/%m/%d')),
                ('bio_text', models.CharField(default='Write Something About Yourself.', max_length=500)),
                ('good', models.IntegerField(default=0)),
                ('fair', models.IntegerField(default=0)),
                ('bad', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('exchangeFavorites', models.ManyToManyField(blank=True, related_name='item_followers', to='exchange.ExchangeItem')),
                ('sellFavorites', models.ManyToManyField(blank=True, related_name='item_followers', to='trade.SellItem')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='myprofile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'ordering': ('created',),
            },
        ),
    ]