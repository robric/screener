import tkinter as tk
import time
from interface.styling_constant import *
from interface.logging_component import Logging
from interface.watchlist_components import Watchlist
from connector.binance_api import BinanceClient

class Root (tk.Tk):
    def __init__(self, testnet:bool):
        super().__init__()
        self.title("Binance Robotor")
        self.configure(bg=BG_COLOR)
        
        self.binance=BinanceClient(testnet=testnet)
        
        self._left_frame=tk.Frame(self,bg=BG_COLOR)
        self._left_frame.pack(side=tk.LEFT)
        self._right_frame=tk.Frame(self,bg=BG_COLOR)
        self._right_frame.pack(side=tk.LEFT)
               
        self._watchlist_frame=Watchlist(self.binance.contracts, self._left_frame, bg=BG_COLOR)
        self._watchlist_frame.pack(side=tk.TOP)
                
        self._logging_frame=Logging(self._left_frame, bg=BG_COLOR)
        self._logging_frame.pack(side=tk.TOP)
        
        self._update_ui()
        
    def _update_ui(self):
        for i,log in enumerate (self.binance.logs):
            if not log['displayed']:
                self._logging_frame.add_log('Index: ' + str(i) + " Date: " + log['log'])
                log['displayed']=True              
        self.after(1500,self._update_ui)
                
    