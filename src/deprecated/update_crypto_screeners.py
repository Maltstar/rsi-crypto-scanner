from datetime import datetime
import requests
import time

## create a list of all crypto screeners
# with (exchange, symbol, desc) and description
def update_crypto_screener():
    ## begin execution time
    start_time = time.time()
    print("start time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("updating crypto screeners...")
    # screener derived from tradinview-list update.py
    screener = ["crypto"]
    screener_data =[]

    r = requests.post(f"https://scanner.tradingview.com/{screener[0]}/scan", data='{"symbols":{"tickers":[],"query":{"types":[]}},"columns":["description"]}')
    for res in r.json()["data"]:
        exchange, symbol = res["s"].split(":")
        desc = res["d"][0]
        data = (exchange, symbol, desc)
        screener_data.append(data)
    print("a total of ",len(screener_data), "screeners were fetched")
    return screener_data

test = update_crypto_screener()
print(test)
