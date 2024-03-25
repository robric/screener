import requests

url = "https://live.euronext.com/pd_es/data/stocks/download?mics=dm_all_stock"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "args[fe_date_format]": "d/m/Y",
    "args[fe_decimal_separator]": ".",
    "args[fe_type]": "csv",
    "args[initialLetter]": "",
    "iDisplayLength": "100",
    "iDisplayStart": "0",
}

response = requests.post(url, headers=headers, data=data)

# Print the response content or save it to a file, as needed
print(response.text)
