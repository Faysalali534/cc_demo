# Generated by Django 3.2.3 on 2021-05-16 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_recordeddata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='input',
            old_name='Currency',
            new_name='currency',
        ),
    ]
