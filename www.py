EURONEXT_WWW='https://live.euronext.com'
ALPHA_WWW='https://www.alphavantage.co'
ALPHA_API_KEY='SAU1C3TCB9Z8VF6C'
NASDAQ_API_KEY='atQwzsXVyLSMuxMxQ8Di'

class target:
    def __init__ (self, site, endpoint, method='GET', params:str={}, data:str={}):
        self.site = site
        self.endpoint = endpoint 
        self.params = params
        self.data = data
        self.method = method

www_us_symbol_list = target (
    site= ALPHA_WWW,
    endpoint='/query',
    params = {
        'function':'LISTING_STATUS',
        'apikey':ALPHA_API_KEY
    }    
)

#
#  All symbols from Euronext are available here: 
#        POST method https://live.euronext.com/en/pd_es/data/stocks?mics=dm_all_stock
#

www_euronext_symbol_list = target (
    method='POST',
    site= EURONEXT_WWW,
    endpoint='/pd_es/data/stocks/download?mics=dm_all_stock',
    data = {
        "args[fe_date_format]": "d/m/Y",
        "args[fe_decimal_separator]": ".",
        "args[fe_type]": "csv",
        "args[initialLetter]": "",
        "iDisplayLength": "100",
        "iDisplayStart": "0",
    }  
)
  


# All symbols from Euronext are available here: 
#        POST method https://live.euronext.com/en/pd_es/data/stocks?mics=dm_all_stock
#


# Request to get quote from nasdaq
#
# curl -X GET 'https://api.nasdaq.com/api/quote/IBM/historical?assetclass=stocks&fromdate=2014-01-29&limit=9999&todate=2024-01-29&random=1' \
# -H 'Accept: application/json, text/plain, */*' \
# -H 'Accept-Language: en-US,en;q=0.9,fr;q=0.8' \
# -H 'Origin: https://www.nasdaq.com' \
# -H 'Referer: https://www.nasdaq.com/' \
# -H 'Sec-Fetch-Dest: empty' \
# -H 'Sec-Fetch-Mode: cors' \
# -H 'Sec-Fetch-Site: same-site' \
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
# -H 'documentLifecycle: active' \
# -H 'frameType: outermost_frame' \
# -H 'initiator: https://www.nasdaq.com' \
# -o output.json


# I removed the following and this still works:
# -H 'Accept-Encoding: gzip, deflate, br' \
#
# Does request support zip unpacking ?