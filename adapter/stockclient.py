import requests
import json
import logging
import pprint as pp

from datetime import datetime
import typing
import pandas as pd 
import numpy as np
import io

import yfinance as yf

from www import *

logger=logging.getLogger()
logger.setLevel("DEBUG")


class StockClient:
    def __init__ (self):
            logger.debug("Class StockClient Initialized...")
            self._headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            self._debug_request=False
            self.symbol_list=self.build_symbol_list()
            
    def _make_request (self, t: target):
        url = t.site + t.endpoint
        logger.debug("_make_request: method %s to URL %s with:", t.method, url)
        logger.debug("      params: %s / data: %s / header=%s ", t.params, t.data, self._headers)
        if t.method=='GET':
            try:
                resp=requests.get(url, headers=self._headers, params=t.params)
            except Exception as e:
                logger.error("GET Error - exception code: %s", e)
        elif t.method=='POST':
            try:
                resp=requests.post(url, headers=self._headers, data=t.data)
            except Exception as e:
                logger.error("POST Error - exception code: %s", e)
        elif t.method=='DELETE':
            try:
                resp=requests.delete(url, headers=self._headers, data=t.data)
            except Exception as e:
                logger.error("DELETE Error - exception code: %s", e)                    
        
        logger.debug("_make_request Status Code is %s ", resp.status_code)
 
        if resp.status_code==200:
            if self._debug_request:
                logger.debug("_make_request response SUCCESS 200 has content %s",resp.text)
            return resp.text
        else:
            logger.error("_make_request error while making the %s request to %s with status %s and content %s",method, url,resp.status_code,r_json)
        return None
    
    def build_symbol_list(self):
        
        # Here we will gather all symbols from exchanges in a single dataframe
        
        df_all = pd.DataFrame()
        
        # Let's start with Euronext data
        
        logger.info("build_symbol_list: ########  fetching symbols for Euronext")
        try:
            raw_data=self._make_request(www_euronext_symbol_list)            
        except Exception as e:
            logger.error("build_symbol_list: Error while making the request for symbol list to EURONEXT code %s",e)
        if raw_data is not None:
            df=pd.read_csv(io.StringIO(raw_data), delimiter=';', skiprows=[1])
            df.to_csv('euro_symbols.csv',index=False)
#
#   The csv information is structured in the following way:
#                                                   Name          ISIN Symbol  ...     Turnover Closing Price Closing Price DateTime
#   0                                        26 Jan 2024           NaN    NaN  ...          NaN           NaN                    NaN
#   1  All datapoints provided as of end of last acti...           NaN    NaN  ...          NaN           NaN                    NaN
#   2                                         1000MERCIS  FR0010285965  ALMIL  ...       235.40         26.60             25/01/2024
#   3                                       2020 BULKERS  BMG9156K1018   2020  ...  22919020.70        145.00             25/01/2024
#   4                                              2CRSI  FR0013341781  AL2SI  ...    558191.24          2.78             25/01/2024
#
            logger.info("build_symbol_list: retrieved dataframe symbol list from euronext, #row is  %s",df.shape[0])
            logger.info("build_symbol_list:  dataframe symbol list from euronext has columns %s",df.keys())

            df=df.iloc[2:]

            df_all['Symbol']=df['Symbol']
            df_all['Name']=df['Name']
            df_all['Exchange']='Euronext'
            df_all['ISIN']=df['ISIN']
            df_all['EuroN Market']=df['Market']
            
            logger.info("build_symbol_list: got the Euronext symbol list to df_all dataframe with this structure: %s",df_all.head(3))
#
#       This is the common structure for all stocks
#
#       Symbol             Name  Exchange          ISIN assetType status
#       ALMIL       1000MERCIS  Euronext  FR0010285965       NaN    NaN
#        2020     2020 BULKERS  Euronext  BMG9156K1018       NaN    NaN
#       AL2SI            2CRSI  Euronext  FR0013341781       NaN    NaN
#        4DDD  3D SYSTEMS CORP  Euronext  US88554D2053       NaN    NaN
#        1DDD  3D SYSTEMS CORP  Euronext  US88554D2053       NaN    NaN


        
        else:
            logger.error("build_symbol_list: Error while getting the symbol list from EURONEXT ")
        
        logger.info("build_symbol_list: ########  fetching symbols for US stocks")
        
        try:
            raw_data=self._make_request(www_us_symbol_list)            
        except Exception as e:
            logger.error("build_symbol_list: Error while making the request for symbol list to US stocks code %s",e)
        if raw_data is not None:
            df = pd.read_csv(io.StringIO(raw_data), delimiter=',')

            logger.info("build_symbol_list: retrieved dataframe symbol list from us, #row is  %s",df.shape[0])
            logger.info("build_symbol_list:  dataframe symbol list from US has columns %s",df.keys())

            df = df.rename(columns={'symbol': 'Symbol', 'name': 'Name', 'exchange': 'Exchange'})
            df = df.drop(columns=['ipoDate','delistingDate'])
            
            df_all = pd.concat ([df_all,df])        
            logger.info("build_symbol_list: concatenate dataframe symbol list with us and euronext, #row is  %s",df_all.shape[0])
            logger.debug("build_symbol_list:  df_all dataframe starts with: %s",df_all.head(5))
            logger.debug("build_symbol_list:  df_all dataframe ends with: %s",df_all.tail(5))

            df_all.to_csv('all_symbols.csv',index=False)
            
        return df_all
    
    
    def get_symbol_history(self, symbol, start_date, end_date):
        
        logger.debug("get_symbol_history: for symbol %s from date %s to date %s",symbol,start_date,end_date)

        """
        Fetch historical stock data from Yahoo Finance.

        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL' for Apple Inc.)
        - start_date: Start date in the format 'YYYY-MM-DD'
        - end_date: End date in the format 'YYYY-MM-DD'

        Returns:
        - DataFrame containing historical stock data with columns: 'Open', 'High', 'Low', 'Close', 'Volume'
        """
        # Fetch historical data from Yahoo Finance
        
        try:
            stock_data = yf.download(symbol, start=start_date, end=end_date)

        except Exception as e:
            logger.error("build_symbol_list: Error while making the request for symbol list to US stocks code %s",e)
            return None
        
        return stock_data

    def get_alpha_vantage_data(self,symbol):
        """
        Fetch historical stock data from Alpha Vantage API for a single symbol.

        Parameters:
        - symbol: Stock symbol (e.g., 'AAPL' for Apple Inc.)

        Returns:
        - DataFrame containing historical stock data
        """
        www_symbol_data = target (
            site= ALPHA_WWW,
            endpoint='/query',
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': ALPHA_API_KEY
            }  
        )
        try:
            data=self._make_request(www_symbol_data)            
        except Exception as e:
            logger.error("get_alpha_vantage_datat: Error code %s",e)
    
        print (data)
        # Convert data to DataFrame
        
        # Convert column data types to numeric

        return data

    def testing(self):

        today_date = datetime.today().strftime('%Y-%m-%d')
        symbol='18M7'
        res = self.get_alpha_vantage_data(symbol)
        print (res.head(10))
 #       data = self.get_symbol_history(symbol, '2020-01-01', today_date)
 #       print (data.head(10))
#        for i in range (10):
#            symbol = self.symbol_list.iloc[i]['Symbol']
#            history = self.get_symbol_history(symbol, '2020-01-01', today_date)
#            print (history.head(10))
        
                    
        
    def build_symbol_history_df(self):

        df_history = pd.DataFrame()
        




        

