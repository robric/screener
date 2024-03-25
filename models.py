from symbol import sym_name
import symbol


class Balance:
    def __init__(self,info):
        self.free = float (info['free'])
        self.locked = float (info['locked'])


class Candles:
    def __init__(self,info):
        self.ts=info[0]
        self.open=float(info[1])
        self.high=float(info[2])
        self.low=float(info[3])
        self.close=float(info[4])
        self.volume=float(info[5])

  # Candles -  list of interval data based on API output with float conversion
  #   [
  #     [
  #       1499040000000,      // Open time
  #       "0.01634790",       // Open
  #       "0.80000000",       // High
  #       "0.01575800",       // Low
  #       "0.01577100",       // Close
  #       "148976.11427815",  // Volume
  #       1499644799999,      // Close time
  #       "2434.19055334",    // Quote asset volume
  #       308,                // Number of trades
  #       "1756.87402397",    // Taker buy base asset volume
  #       "28.46694368",      // Taker buy quote asset volume
  #       "17928899.62484339" // Ignore.
  #     ]
  #  ]
  
  
class Contracts:
  def __init__(self,params):
      self.symbol=params['symbol']
      self.info=params

        
# API endpoint  
# 
# {
#  "timezone": "UTC",
#  "serverTime": 1565246363776,
#  "rateLimits": [
#    {
#      //These are defined in the `ENUM definitions` section under `Rate Limiters (rateLimitType)`.
#      //All limits are optional
#    }
#  ],
#  "exchangeFilters": [
#    //These are the defined filters in the `Filters` section.
#    //All filters are optional.
#  ],
#  "symbols": [
#    {
#      "symbol": "ETHBTC",
#      "status": "TRADING",
#      "baseAsset": "ETH",
#      "baseAssetPrecision": 8,
#      "quoteAsset": "BTC",
#      "quotePrecision": 8,
#      "quoteAssetPrecision": 8,
#      "orderTypes": [
#        "LIMIT",
#        "LIMIT_MAKER",
#        "MARKET",
#        "STOP_LOSS",
#        "STOP_LOSS_LIMIT",
#        "TAKE_PROFIT",
#        "TAKE_PROFIT_LIMIT"
#      ],
#      "icebergAllowed": true,
#      "ocoAllowed": true,
#      "quoteOrderQtyMarketAllowed": true,
#      "allowTrailingStop": false,
#      "cancelReplaceAllowed": false,
#      "isSpotTradingAllowed": true,
#      "isMarginTradingAllowed": true,
#      "filters": [
#        //These are defined in the Filters section.
#        //All filters are optional
#      ],
#      "permissions": [
#         "SPOT",
#         "MARGIN"
#      ]
#    }
#  ]
#}


class OrderStatus:
  def __init__(self,info):
      self.symbol=info['symbol']
      self.orderId=info['orderId']
      self.status=info['status']
      self.price=info['price']
      self.origQty=info['origQty']
      self.executedQty=info['executedQty']
  def dump(self):
      return {'symbol': self.symbol,'orderID': self.orderId,'status':self.status,'price':self.price,'origQty':self.origQty,'executedQty':self.executedQty}
      
           
# Query Order 
# 
# {
#   "symbol": "LTCBTC",
#   "orderId": 1,
#   "orderListId": -1, //Unless OCO, value will be -1
#   "clientOrderId": "myOrder1",
#   "price": "0.1",
#   "origQty": "1.0",
#   "executedQty": "0.0",
#   "cummulativeQuoteQty": "0.0",
#   "status": "NEW",
#   "timeInForce": "GTC",
#   "type": "LIMIT",
#   "side": "BUY",
#   "stopPrice": "0.0",
#   "icebergQty": "0.0",
#   "time": 1499827319559,
#   "updateTime": 1499827319559,
#   "isWorking": true,
#   "origQuoteOrderQty": "0.000000"
# }