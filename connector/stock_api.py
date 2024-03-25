

# from ast import Or
# from this import d
import requests
import json
import logging
# from sqlalchemy import false
from   constant import *
import pprint as pp
import time
import hmac
import hashlib
import websocket
from urllib.parse import urlencode
import threading
from models import *
import typing
import pandas as pd 
import numpy as np
import io
from tradingview_ta import TA_Handler, Interval, Exchange

logger=logging.getLogger()
logger.setLevel("DEBUG")

class StockClient:
    def __init__ (self):

        self._iex_base_url=IEX_API
        _iex_keys=self._get_keys("iex_key.txt")
            
        self._iex_public_key=_iex_keys['public_key']
        self._iex_secret_key=_iex_keys['secret_key']
        self._headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
    #    self._ws=None
    #    self.prices=dict()
    #    self._ws_id=1
        
    #    self.symbols=self.get_symbols()
    #    self.balance=self.get_balance()

        self.logs = []
        
    #    t = threading.Thread(target=self._start_ws)
    #    t.start()
        
        logger.debug("Class StockClient Initialized...")

# This method extracts the private and public keys from a local file 
#
# public_key=123456789abcd...
# secret_key=123efb34...
#
# returns a dict {'public_key':xxx,'secret_key':xx}
# 
    def add_logs (self, msg:str):
        logger.debug("add_logs debug: %s",msg)
        self.logs.append({'log':msg,'displayed':False})
        
    def _get_keys (self,file_name:str) -> typing.Dict:
        f=open(file_name,'r')
        keys=dict()
        for line in f:
            k,v=line.split("=")
            if k in ['public_key','secret_key']:
               keys[k]=v.strip()
        return keys
    
   # def _generate_signature (self,data: dict) -> str:
   #     return hmac.new(self._secret_key.encode(),msg=urlencode(data).encode(),digestmod=hashlib.sha256).hexdigest()

    def _make_request (self, method: str, endpoint: str, provider: str, data: dict=None, signed=False):
    #    if signed:
    #        data['timestamp']=int(time.time()*1000)
    #        data['signature']=self._generate_signature(data)
    #    
        if data is None:
            data = {}
            
        if provider == 'IEX':
            data['token'] = self._iex_secret_key
            url = self._iex_base_url + endpoint
        elif provider == 'EURONEXT':
            url = EURONEXT_WWW + endpoint
        elif provider == 'ALPHA':
            url = ALPHA_WWW + endpoint
            
        logger.debug("_make_request: method %s to URL %s with signed=%s params=%s header=%s ", method, url, signed, data, self._headers)
        if method=='GET':
            try:
                resp=requests.get(url, headers=self._headers, params=data)
            except Exception as e:
                logger.error("Connection Error with method %s, exception code: %s", method, e)
        elif method=='POST':
            try:
                resp=requests.post(url, headers=self._headers, data=data)
            except Exception as e:
                logger.error("Connection Error with method %s, exception code: %s", method, e)
        elif method=='DELETE':
            try:
                resp=requests.delete(url, headers=self._headers, data=data)
            except Exception as e:
                logger.error("Connection Error with method %s, exception code: %s", method, e)                    
#        try:
#            r_json=resp.json()
#        except ValueError:            
#            logger.error("Error empty json content while making the %s request to %s with status %s",method,self._base_url+endpoint,resp.status_code)
#            return None
#        
        logger.debug("Request Status Code is %s ", resp.status_code)
 
        if resp.status_code==200:
            logger.debug("_make_request response SUCCESS 200 to %s with params=%s has content %s",url,data,resp.text)
            return resp.text
        else:
            logger.error("Error while making the %s request to %s with status %s and content %s",method, url,resp.status_code,r_json)
        return None
#    
#    def get_symbols(self) -> typing.Dict[str, Contracts]:        
#        raw_data=self._make_request("GET",EP['iex_symbols'],None,provider='iex')        
#        symbols=dict()
#        if raw_data is not None:
#            for s in raw_data:
#                symbols[s['symbol']]=s
#        return symbols
#    
    def get_symbol_list(self,exchange):
        if exchange==EX_EURONEXT:
            data = {
                "args[fe_date_format]": "d/m/Y",
                "args[fe_decimal_separator]": ".",
                "args[fe_type]": "csv",
                "args[initialLetter]": "",
                "iDisplayLength": "100",
                "iDisplayStart": "0",
            }
            try:
                data=self._make_request('POST',EP['euro_symbols'],data=data,provider='EURONEXT')            
            except:
                logger.error("get_symbol_list: Error while making the request for symbol list to EURONEXT ")
                return None
        if exchange==EX_NYSE:
            data = {
                'function':'LISTING_STATUS',
                'apikey':ALPHA_API_KEY
            }
            try:
                data=self._make_request('GET',EP['alpha_query'],data=data,provider='ALPHA')            
            except Exception as e:
                logger.error("get_symbol_list: Error while making the request for NYSE symbol list to Alpha with code : %s",e)
                return None
        return data
    
    def init_symbols_db(self):
        df_all_symbols = pd.DataFrame()
        
        raw_data=self.get_symbol_list(EX_EURONEXT)
        if raw_data is not None:
            df=pd.read_csv(io.StringIO(raw_data), delimiter=';', skiprows=[1])
            df_all_symbols['Symbol']
            df.to_csv('euro_symbols.csv',index=False)
            print (df.head(10))
        else:
            logger.error("store_symbols: Error while getting the symbol list from EURONEXT ")
    
    
    def history_candles(self,symbol: str,interval: str) -> typing.List[Candles]:
        data=dict()
        data={
            'symbol':contract.symbol,
            'interval':interval,
            'limit':1000
            }
        raw_candles=self._make_request('GET',EP['candles'],data)
        candles=[]
        if raw_candles is not None:
            for c in raw_candles:
                candles.append(Candles(c))
       
        return candles
 #
 # This method creates a dict with 'bid' and 'ask' _keys for a symbol
 #   
    def get_bid_ask(self,contract: Contracts) -> typing.Dict[str, float]:
        data=dict()
        symbol=contract.symbol
        data['symbol']=symbol
        resp=self._make_request("GET",EP['bookticker'],data)
        logger.debug("get_bid_ask for %s: returned=%s",symbol,resp)
        
        if resp is not None:
            if symbol not in self.prices:
                self.prices[symbol]={'bid':float(resp['bidPrice']),'ask':float(resp['askPrice'])}
            else:    
                self.prices[symbol]['bid']=float(resp['bidPrice'])
                self.prices[symbol]['ask']=float(resp['askPrice'])           
            return self.prices[symbol]
    
    def get_balance(self) -> typing.Dict[str, Balance]:
        data=dict()
        balances=dict()
        account_data=self._make_request("GET",EP['account'],data,signed=True)
        if account_data is not None:
            for a in account_data['balances']:
                balances[a['asset']]=Balance(a)
        return balances

#  Call API for orders.
#  
#  Example of expected parameters for order API
#  params = {
#      "symbol": "BNBUSDT",
#      "side": "BUY",
#      "type": "LIMIT",
#      "timeInForce": "GTC",
#      "quantity": 1,
#      "price": "20",
#  }    
    def place_order(self, contract: Contracts, side: str,type: str, price=None,quantity=None,tif=None) -> OrderStatus:
        data=dict()
        data['symbol']=contract.symbol
        data['side']=side
        data['type']=type
        if quantity is not None:
            data['quantity']= round(quantity / contract.lot_size) * contract.lot_size
            print ("qqqqqqqq",data['quantity'])
        if price is not None:
            data['price']=round(round(price / contract.tick_size) * contract.tick_size,8)
        if tif is not None:
            data['timeInForce']=tif
        resp=  self._make_request('POST',EP['order'],data,signed=True)
        if resp is not None:
            order_status=OrderStatus(resp)          
        return order_status
    
    def cancel_order(self, contract: Contracts, orderId: int) -> OrderStatus:
        data= dict()
        data['symbol']= contract.symbol
        data['orderId']= orderId
        resp=self._make_request('DELETE',EP['order'],data,True)
        if resp is not None:
            order_status=OrderStatus(resp)        
        return order_status
    
    def get_order_status(self, contract: Contracts, orderId: int) -> OrderStatus:
        data=dict()
        data['symbol']=contract.symbol
        data['orderId']=orderId
        resp=self._make_request('GET',EP['order'],data,True)
        if resp is not None:
            order_status=OrderStatus(resp)
        return order_status
    
    def ping_binance_api(self):
        return self._make_request('GET',EP['ping'],"")
    
    def _start_ws (self):
        self._ws = websocket.WebSocketApp(self._wss_url,on_open=self._on_open, on_close=self._on_close, on_error=self._on_error, on_message=self._on_message)
        while True:
            try:
                self._ws.run_forever()
            except Exception as e:
                logger.error("Websocket interrupted code: %s", e)
            time.sleep(2)
    
    def _on_open (self,ws):
        logger.info ("websocket connection established in %s mode to %s",self._mode,self._wss_url)
        self.subscribe_channel(list(self.contracts.values()),"bookTicker")
        return
    
    def _on_close (self,ws):
        logger.warning ("websocket connection was closed")
        return
    
    def _on_error (self,ws, msg):
        logger.error ("websocket connection error with code: %s",msg)
        return

#
#   on_message update: format or Websocket messages is
#   {"u":27556606859,"s":"BTCUSDT","b":"16786.54000000","B":"0.00069000","a":"16787.13000000","A":"0.10000000"}
#

    def _on_message (self, ws, msg):
        logger.debug ("websocket connection message:  %s",msg)
        data=json.loads(msg) 
        if 's' in data: 
            symbol=data['s']
            if symbol not in self.prices:
                self.prices[symbol]={'bid':float(data['b']),'ask':float(data['a'])}
            else:    
                self.prices[symbol]['bid']=float(data['b'])
                self.prices[symbol]['ask']=float(data['a'])
            if symbol == 'BTCBUSD':
                self.add_logs("SYMBOL: " + symbol + "  bid = " + str(self.prices[symbol]['bid']) + " / ask = " + str(self.prices[symbol]['ask']))
                
            return self.prices[symbol]
        else:
            return None
    
    def subscribe_channel(self, contracts:typing.List[Contracts],channel: str):
        data={
            'method':"SUBSCRIBE",
            'id':self._ws_id,
            'params':[]
        }
        for c in contracts:
            data['params'].append(c.symbol.lower()+"@"+channel)
        self._ws_id+=1
        logger.debug ("websocket subscription to with data: %s",json.dumps(data))
        try:
            self._ws.send(json.dumps(data))
        except Exception as e:
            logger.error("Connection Error with websocket with data %s, code: %s", json.dumps(data), e)           
        return
