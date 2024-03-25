from multiprocessing.connection import wait
import tkinter as tk
import logging
import time
import os
import pandas as pd

import requests
from connector.stock_api import StockClient
from constant import *
from interface.styling_constant import *
# from interface.root_component import *
from tradingview_ta import TA_Handler, Interval, Exchange

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

logger=logging.getLogger()
logger.setLevel("DEBUG")
formatter=logging.Formatter('%(asctime)s - %(levelno)s - %(levelname)s : %(message)s')

stream_h=logging.StreamHandler()
stream_h.setFormatter(fmt=formatter)
stream_h.setLevel(logging.DEBUG)
logger.addHandler(stream_h)

file_h=logging.FileHandler('info.log')
file_h.setFormatter(formatter)
file_h.setLevel(logging.DEBUG)
logger.addHandler(file_h)

#
# Reminder: this lib permits to write proper syslog messages with levels
# logger.info("test info foo")
# logger.critical("test info bar")
#

print('A')
if __name__ == "__main__":
    
#    bc=BinanceClient(testnet=True)
#    root = Root(testnet=True)
#    root.mainloop()
#   
    print("START")
    sc = StockClient()
    sc.store_symbols()
    print("END")



#    print (bc.get_balance())
#    print (bc.get_contracts()['BTCBUSD'].tick_size)

#   print ("precision =",bc.contracts['ETHBUSD'].quotePrecision,"",bc.contracts['ETHBUSD'].quoteAssetPrecision)
#   print (bc.contracts.values())
#   print (bc.history_candles("BTCBUSD"))
    
 #   test=bc.place_order("BNBUSDT","BUY","LIMIT",quantity=0.1,price=400,tif="GTC")
 #   print (test)
    

#    contracts= bc.get_con
#  tracts()
 
#    candles=bc.history_candles('BTCBUSD','5m')
#
#    print (bc.get_bid_ask('BTCBUSD'))
    
 #   root = tk.Tk()
 #   i=0
 #   for c in contracts:
 #       Labels=tk.Label(root, text=c,borderwidth=1,relief=tk.SOLID,fg='black',bg='gold',width=15)
 #       Labels.grid(row=i % C.ROW_NUM,column= i // C.ROW_NUM, sticky='ew')
 #       i+=1
 #   
 #   root.mainloop()

    
    







