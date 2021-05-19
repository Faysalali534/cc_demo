from celery import shared_task

from time import sleep

from main.api import ExchangeManipulation
from main.models import Input


@shared_task(bind=True)
def generate_balance_and_leger(self, pk_num):
    sleep(15)
    input_instance = Input.objects.get(pk=pk_num)
    exchange_manipulation = ExchangeManipulation(
        start_date=input_instance.start_date,
        end_date=input_instance.end_date,
        currency=input_instance.currency.name,
        category=input_instance.category,
        exchange_id=input_instance.exchange.name,
        api_key=input_instance.account.api_key,
        secret_key=input_instance.account.secret_key,
        input_instance=input_instance,
    )
    exchange_manipulation.generate_balance_and_leger()
    return "ok"
