from django.contrib import admin

# Register your models here.
from main.models import Account
from main.models import Input
from main.models import Currency
from main.models import RecordedData
from main.models import Exchange

admin.site.register(Account)
admin.site.register(Input)
admin.site.register(Currency)
admin.site.register(RecordedData)
admin.site.register(Exchange)



