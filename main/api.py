import ccxt


def get_client(exchange_id, api_key, secret):
    """
    Returns the exchange
    :param str exchange_id: id
    :param str api_key: API key
    :param str secret: Secret
    :return: Exchange
    """
    exchange_class = getattr(ccxt, exchange_id)
    return exchange_class(
        {
            "apiKey": api_key,
            "secret": secret,
            "timeout": 1000,
            "enableRateLimit": True,
            'options': {
                'defaultType': 'inverse',  # exchange-specific option
            }
        }
    )
