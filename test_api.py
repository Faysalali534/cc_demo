import ccxt
from pprint import pprint



# s299o7liRLmO8gxSq14M2JMAxY7yXQsJQA3a -> secret

# mqLu1EHk8l4RWfk3Kc
# testing for bybit exchange
exchange = ccxt.bybit({
    'apiKey': 'mqLu1EHk8l4RWfk3Kc',
    'secret': 's299o7liRLmO8gxSq14M2JMAxY7yXQsJQA3a',
    'rateLimit': 100,  # unified exchange property
    'options': {
        'adjustForTimeDifference': True,
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

