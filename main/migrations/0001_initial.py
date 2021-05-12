# Generated by Django 3.2.2 on 2021-05-12 21:38

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('short_code', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange', models.CharField(choices=[('binance', 'Binance'), ('bybit', 'Bybit')], max_length=250)),
                ('api_key', models.CharField(max_length=250)),
                ('secret', models.CharField(max_length=250)),
                ('password', models.CharField(blank=True, max_length=250, null=True)),
                ('default_fee_rate', models.DecimalField(decimal_places=4, default=Decimal('0.1000000000000000055511151231257827021181583404541015625'), max_digits=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
