from datetime import datetime

import ccxt

from main.models import RecordedData


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
        client = self._get_client()
        client.set_sandbox_mode(True)
        balance = client.fetch_balance({'coin': self.currency})
        # ledger = client.fetch_ledger(params={"wallet_fund_type": "RealisedPNL"})
        ledger = client.fetch_ledger(params={"currency": self.currency})
        self._get_realised_pnl(balance=balance, ledger=ledger)
        print()

    def _get_realised_pnl(self, balance, ledger):
        realised_pnl = balance["info"]["result"][self.currency].get("realised_pnl")
        for data in ledger:
            ledger_id = data.get("id")
            amount = data.get("amount")
            before = data.get("before")
            after = data.get("after")
            transaction_time = data.get("datetime")
            captured_date = datetime.strptime(transaction_time[:-1], '%Y-%m-%dT%H:%M:%S.%f')
            type = data.get("info")["type"]
            RecordedData.objects.create(
                type=type,
                after=after,
                captured_date=captured_date,
                ledger_id=ledger_id,
                Input=self.input_instance,
                before=before,
                amount=amount,
            )
