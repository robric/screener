import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


def get_iex_symbols(api_token):
    url = 'https://cloud.iexapis.com/stable/ref-data/symbols'
    params = {'token': api_token}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        symbols = [stock['symbol'] for stock in data]
        return symbols
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def get_stock_info(symbol, api_token):
    url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote'
    params = {'token': api_token}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data for symbol {symbol}: {response.status_code}")
        return None
  

options = webdriver.ChromeOptions() 
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
  
driver = webdriver.Chrome(options=options)
driver.get("https://live.euronext.com/en/products/equities/list")

outer_div = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.dt-buttons.d-flex.align-items-center"))
)


download_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-link')]"))  
)




download_btn.click()


while True:
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='table-responsive']")))
        break
    except:
        pass

# # Example usage:
# api_token = 'sk_7f20073bbf4a4bd9b744c5a04eaab5ee'  # Replace with your actual API token from IEX Cloud
# symbols = get_iex_symbols(api_token)
# #print(symbols,len(symbols))
# 
# my_stock=symbols[0]
# 
# sk_info = get_stock_info(my_stock, api_token)
# print(sk_info)
# 
# print (my_stock)

# Example usage:
# pub_api_key="pk_d70edef383a84e1da6c718a9f5dca933"
# api_key = 'sk_7f20073bbf4a4bd9b744c5a04eaab5ee'  # Replace with your actual API key from Financial Modeling Prep
# all_symbols = get_all_symbols(pub_api_key)
# print(all_symbols)
