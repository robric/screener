from multiprocessing.connection import wait
import tkinter as tk
import logging
import time
import os

import requests
from adapter.stockclient import StockClient


if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

logger=logging.getLogger()
logger.setLevel("DEBUG")
formatter=logging.Formatter('%(asctime)s - %(levelno)s - %(levelname)s : %(message)s')

stream_h=logging.StreamHandler()
stream_h.setFormatter(fmt=formatter)
stream_h.setLevel(logging.INFO)
logger.addHandler(stream_h)

file_d=logging.FileHandler('debug.log')
file_d.setFormatter(formatter)
file_d.setLevel(logging.DEBUG)
logger.addHandler(file_d)

file_i=logging.FileHandler('info.log')
file_i.setFormatter(formatter)
file_i.setLevel(logging.INFO)
logger.addHandler(file_i)

#
# Reminder: this lib permits to write proper syslog messages with levels
# logger.info("test info foo")
# logger.critical("test info bar")
#

if __name__ == "__main__":
    
#    bc=BinanceClient(testnet=True)
#    root = Root(testnet=True)
#    root.mainloop()
#   
    print("START")
    sc = StockClient()
    sc.testing()
    
#    sc.store_symbols()
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

    
    







