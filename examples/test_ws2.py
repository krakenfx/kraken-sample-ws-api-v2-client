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

# time.sleep(3)

# Sample order-entry call:

my_client.request(
    # Insert method and params as described in the docs
    request = {
        'method': 'add_order',
        'params': {
            'limit_price': 10010.10,
            'order_type': 'limit',
            'order_userref': 121,
            'order_qty': 0.0001,
            'side': 'buy',
            'symbol': 'BTC/EUR',
            'token': my_websockets_token
        }
    },
    req_id = 1234567892,
    callback = my_handler
)

time.sleep(3)

my_client.request(
    # Insert method and params as described in the docs
    request = {
        'method': 'add_order',
        'params': {
            'limit_price': 10011.10,
            'order_type': 'limit',
            'order_userref': 121,
            'order_qty': 0.01,
            'side': 'sell',
            'symbol': 'ETH/EUR',
            'token': my_websockets_token
        }
    },
    req_id = 1234567892,
    callback = my_handler
)

time.sleep(3)

my_client.request(
    request = {
        'method': 'cancel_all',
        'params': {
            'token': my_websockets_token
        },
    },
    req_id = 1234567893,
    callback = my_handler
)
