# Generated by Django 3.2.3 on 2021-05-20 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_recordeddata_roi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(default='')),
                ('status', models.CharField(default='successful', max_length=30)),
                ('input', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.input')),
            ],
        ),
    ]
