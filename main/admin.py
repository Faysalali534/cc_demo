from django.contrib import admin

# Register your models here.
from main.models import Account
from main.models import Input
from main.models import Currency

admin.site.register(Account)
admin.site.register(Input)
admin.site.register(Currency)


