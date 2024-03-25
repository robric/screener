import tkinter as tk
import typing
from models import *

from interface.styling_constant import *

class Watchlist(tk.Frame):
    def __init__(self, binance_contracts: typing.Dict[str,Contracts], *args, **kwargs):
        super().__init__(*args, **kwargs) 
        
        self.binance_symbols = list (binance_contracts.keys())
        print (self.binance_symbols)
        
        self._commands_frame = tk.Frame(self,bg=BG_COLOR)
        self._commands_frame.pack(side=tk.TOP)
        
        self._table_frame = tk.Frame (self,bg=BG_COLOR)
        self._table_frame.pack (side='top')
        
        self._binance_label = tk.Label(self._commands_frame,text='Binance',bg=BG_COLOR, fg=FG_COLOR)
        self._binance_label.grid(row=0,column=0)
        
        self._binance_entry = tk.Entry(self._commands_frame,fg=FG_COLOR,justify=tk.CENTER, insertbackground=FG_COLOR,bg=BG_COLOR2)
        self._binance_entry.grid(row=1,column=0)
        self._binance_entry.bind("<Return>",self._add_binance_symbol)
        
        self.headers = ['symbol','exchange','bid','ask']
        
        for idx, h in enumerate(self.headers):
            header = tk.Label(self._table_frame,text=h.capitalize(),bg=BG_COLOR,fg=FG_COLOR,font=BOLD_FONT)
            header.grid(row=0,column=idx)

    def _add_binance_symbol(self,event):
        symbol = event.widget.get()
        self._add_symbol(symbol,"Binance")
        event.widget.delete(0,tk.END)
    
    def _add_symbol(self, symbol:str, exchange:str):
        return