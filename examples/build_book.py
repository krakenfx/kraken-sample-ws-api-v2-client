import zlib
from kraken_wsclient_v2 import kraken_wsclient_v2 as client

checksumLength = 10

symbolPrecision = {'BTC/GBP': {'price': 1, 'qty': 8}, 'BTC/USD': {'price': 1, 'qty': 8},
                   'ETH/EUR': {'price': 2, 'qty': 8}, 'ETH/USD': {'price': 2, 'qty': 8},
                   'ADA/BTC': {'price': 8, 'qty': 8}, 'MANA/ETH': {'price': 7, 'qty': 8}}

class OrderBook:
    '''This is an updated traffic light class'''
    def __init__(self):
        self.book = {}

    def onMessage(self, message):
        if message['type'] == 'snapshot':
            self.createBook(message)
        else:
            self.updateBook(message)


    def createBook(self, message):
        for i in message['data']:
                symbol = i['symbol']
                self.book.update({symbol: {'asks': {}, 'bids': {}, 'depth': len(i['asks']),
                                           'serverChecksum': i['checksum'], 'localChecksum': i['checksum']}})
                for ask in i['asks']:
                    self.book[symbol]['asks'].update({ask['price']: ask['qty']})

                for bid in i['bids']:
                    self.book[symbol]['bids'].update({bid['price']: bid['qty']})


    def updateBook(self, message):
        for i in message['data']:
                symbol = i['symbol']
                for ask in i['asks']:
                     if ask['qty'] != 0.0:
                          self.book[symbol]['asks'].update({ask['price']: ask['qty']})
                     else:
                          self.book[symbol]['asks'].pop(ask['price'])

                for bid in i['bids']:
                     if bid['qty'] != 0.0:
                          self.book[symbol]['bids'].update({bid['price']: bid['qty']})
                     else:
                          self.book[symbol]['bids'].pop(bid['price'])

                # print('len asks before:', len(self.book[symbol]['asks']))
                # print('len bids before:', len(self.book[symbol]['bids']))
                if i['asks'] != []:
                    self.book[symbol]['asks'] = dict(sorted(self.book[symbol]['asks'].items())[:self.book[symbol]['depth']])
                if i['bids'] != []:
                    self.book[symbol]['bids'] = dict(sorted(self.book[symbol]['bids'].items(), reverse=True)[:self.book[symbol]['depth']])
                # print('len asks after:', len(self.book[symbol]['asks']))
                # print('len bids after:', len(self.book[symbol]['bids']))

                self.book[symbol]['serverChecksum'] = i['checksum']
                self.checkChecksum(symbol)



    def handleZeros(self, value, precision):
        zerosPrice = '.' + str(precision) + 'f'
        # add zeros in the end:
        res = f"{value:,{zerosPrice}}"
        # remove . and , from the string:
        res = res.replace('.', '')
        res = res.replace(',', '')
        # remove leading zeros:
        while res[0] == '0':
            res = res[1:]
        return res


    def checkChecksum(self, symbol):
        # get symbol price and qty precision
        precisionPrice = symbolPrecision[symbol]['price']
        precisionQty   = symbolPrecision[symbol]['qty']

        sortedAsks = sorted(self.book[symbol]['asks'].items())[:checksumLength]
        data = ''
        for i in sortedAsks:
            data += self.handleZeros(i[0], precisionPrice)
            data += self.handleZeros(i[1], precisionQty)

        sortedBids = sorted(self.book[symbol]['bids'].items(), reverse=True)[:checksumLength]

        for i in sortedBids:
            data += self.handleZeros(i[0], precisionPrice)
            data += self.handleZeros(i[1], precisionQty)

        data = bytes(data, 'utf-8')
        self.book[symbol]['localChecksum'] = zlib.crc32(data)


myOrderBook = OrderBook()

def my_handler(message):
    # Here you can do stuff with the messages
    # print(message)
    if 'channel' in message:
        if message['channel'] == 'book':
            myOrderBook.onMessage(message)
    print()
    print('Here goes book:')
    print(myOrderBook.book)


my_client = client.WssClient()
my_client.start()

# Sample public-data subscription:

my_client.subscribe_public(
    # Insert params and req_id as described in the docs
    params = {
        'channel': 'book',
        'depth': 10,
        'snapshot': True,
        'symbol': ['MANA/ETH'],
    },
    req_id = 1234567890,
    callback = my_handler
)
