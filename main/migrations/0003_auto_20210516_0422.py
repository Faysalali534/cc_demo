# Generated by Django 3.2.3 on 2021-05-16 04:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_input_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='api_keys',
            new_name='api_key',
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='input',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.account'),
        ),
    ]
