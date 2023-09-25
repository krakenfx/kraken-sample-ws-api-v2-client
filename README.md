# Kraken WebSockets Client v2 in Python

Sample Kraken WebSockets client in Python.  This client was created for
demonstration purposes only.  It is neither maintained nor supported.

## Installation

    pip install kraken-wsclient-v2-py

## Sample Usage

    import time

    from kraken_wsclient_v2 import kraken_wsclient_v2 as client

    def my_handler(message):
        # Here you can do stuff with the messages
        print(message)

    my_websockets_token = ''

    my_client = client.WssClient()
    my_client.start()

    # Sample public-data subscription:

    my_client.subscribe_public(
        # Insert params and req_id as described in the docs
        params = {
            'channel': 'ticker',
            'snapshot': True,
            'symbol': ['BTC/USD', 'XRP/USD'],
        },
        req_id = 1234567890,
        callback = my_handler
    )

    time.sleep(3)

    # Sample private-data subscription:

    my_client.subscribe_private(
        # Insert params and req_id as described in the docs
        params = {
            'channel': 'executions',
            'snapshot': True,
            'snapshot_trades': True,
            'order_status': True,
            'ratecounter': True,
            'token': my_websockets_token
        },
        req_id = 1234567891,
        callback = my_handler
    )

## Compatibility

This code has been tested on Python 3.7.

## Contributing

Pull requests are not monitored and likely will be ignored.
