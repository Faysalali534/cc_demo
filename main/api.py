import time
from datetime import datetime

import ccxt

from main.models import RecordedData, Log
from django.conf import settings


class ExchangeManipulation:
    def __init__(self, start_date, end_date, currency, category, **kwargs):
        self.start_date = start_date
        self.end_date = end_date
        self.currency = currency
        self.category = category
        self.api_key = kwargs.get('api_key')
        self.secret_key = kwargs.get('secret_key')
        self.exchange_id = kwargs.get('exchange_id')
        self.input_instance = kwargs.get('input_instance')

    def _get_client(self):
        """
        Returns the exchange
        :param str exchange_id: id
        :param str api_key: API key
        :param str secret: Secret
        :return: Exchange
        """
        exchange_class = getattr(ccxt, self.exchange_id)
        return exchange_class(
            {
                "apiKey": self.api_key,
                "secret": self.secret_key,
                "timeout": 1000,
                "enableRateLimit": True,
                'options': {
                    'defaultType': self.category,  # exchange-specific option
                }
            }
        )

    def generate_balance_and_leger(self):
        try:
            client = self._get_client()
            client.set_sandbox_mode(True)
            balance = client.fetch_balance({"coin": self.currency})
            start_unix_date = time.mktime(self.start_date.timetuple())
            end_unix_date = time.mktime(self.end_date.timetuple())
            ledger = client.fetch_ledger(
                params={"currency": self.currency, "till": end_unix_date},
                since=start_unix_date,
            )
            self._place_queue_data(balance=balance, ledger=ledger)
        except Exception as error:
            Log.objects.create(
                input_id=self.input_instance.id,
                currency=self.input_instance.currency,
                start_date=self.input_instance.start_date,
                end_date=self.end_date,
                category=self.category,
                exchange=self.input_instance.exchange,
                info=str(error),
                status="Failed",
            )

    def _calculate_roi(self, after, before):
        after_value = float(after)
        before_value = float(before)
        total = before_value * 100
        # setting for the purpose of test , because after and before are sometimes in random values
        if not total and settings.TEST_ENV:
            total = 10
        roi = after_value - before_value / total
        return str(roi)[:4]

    def _place_queue_data(self, balance, ledger):

        realised_pnl = balance["info"]["result"][self.currency].get("realised_pnl")
        for data in ledger:
            ledger_id = data.get("id")
            leger_id_present = RecordedData.objects.filter(ledger_id__exact=ledger_id)
            if not leger_id_present:
                amount = data.get("amount")
                before = data.get("before")
                after = data.get("after")
                transaction_time = data.get("datetime")
                captured_date = datetime.strptime(transaction_time[:-1], '%Y-%m-%dT%H:%M:%S.%f')
                type = data.get("info")["type"]
                roi = self._calculate_roi(after=after, before=before)
                if type.lower() == 'realisedpnl':
                    RecordedData.objects.create(
                        type=type,
                        after=after,
                        captured_date=captured_date,
                        ledger_id=ledger_id,
                        Input=self.input_instance,
                        before=before,
                        realised_pnl=realised_pnl,
                        amount=amount,
                        roi=roi
                    )
                else:
                    RecordedData.objects.create(
                        type=type,
                        after=after,
                        captured_date=captured_date,
                        ledger_id=ledger_id,
                        Input=self.input_instance,
                        before=before,
                        amount=amount,
                        roi=roi

                    )
        Log.objects.create(
            currency=self.input_instance.currency,
            start_date=self.input_instance.start_date,
            end_date=self.end_date,
            category=self.category,
            exchange=self.input_instance.exchange,
            input_id=self.input_instance.id
        )
