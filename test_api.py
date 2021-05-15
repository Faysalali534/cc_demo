import ccxt
from pprint import pprint

# testing for bybit exchange
exchange = ccxt.bybit({
    'apiKey': 'tfiebTVMW7HMsxttfH',
    'secret': '4EUUZvoQj0WboHOQDp5PsJC8YdwhKPM5YpvA',
    'rateLimit': 100,  # unified exchange property
    'options': {
        'defaultType': 'inverse',  # exchange-specific option
    }
})
# setting the sandbox mode to use the testnet account
exchange.set_sandbox_mode(True)

# fetch balance
balance = exchange.fetch_balance({'coin': 'BTC'})
ledger = exchange.fetch_ledger(params={"wallet_fund_type": "RealisedPNL"})
ledger = exchange.fetch_ledger()
pprint(balance)
print('Ledger ->')
pprint(ledger)
pprint(len(ledger))

