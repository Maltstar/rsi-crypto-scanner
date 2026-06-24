import os
from polygon import RESTClient
from dotenv import load_dotenv



def get_restclient():

    # load environment variable
    load_dotenv()

    # import API KEY and URL to fetch cryptos rank
    api_key_pol = os.environ['POL_API_KEY']
    # create rest client
    client = RESTClient(api_key_pol)

    return client


# creating client to communicate with the api
#client = RESTClient(api_key_pol)

# fetch rsi from given ticker parameters and client
def fetch_rsi_standalone(client, ticker="X:BTCUSD",timespan="day", window="21", series_type="close", order="desc", limit='10' ):

    rsi = client.get_rsi(
        ticker=ticker,
        timespan=timespan,
        window=window,
        series_type=series_type,
        order=order,
        limit=limit,
    )

    print('rsi',rsi)

    return rsi

# 1- create client
# 2- fetch rsi
def fetch_rsi(ticker="X:BTCUSD",timespan="day", window="21", series_type="close", order="desc", limit='10' ):

    #load_dotenv()

    # import API KEY and URL to fetch cryptos rank
    #api_key_pol = os.environ['POL_API_KEY']
    client = get_restclient()

    rsi = client.get_rsi(
        ticker=ticker,
        timespan=timespan,
        window=window,
        series_type=series_type,
        order=order,
        limit=limit,
    )

    print('rsi',rsi)

    return rsi

    #rsi_values = rsi.values
   # print('rsi_values', rsi_values)

   # print('rsi_values 1st element', rsi_values[0])
   # print('rsi_values 1st element', rsi_values[0].timestamp)

'''
calculate the rsi ohcl4
1 - fetch the 4 different rsi (close, open, low, high) and
2 - calculate the average mean to obtain the rsi ohcl4
'''
def calculate_rsi_ochl4(ticker="X:BTCUSD"):

    #fetching rsi close, per default the serie type is 'close'
    result_rsi_close = fetch_rsi()
    rsi_close_values = result_rsi_close.values

    #fetching rsi open
    result_rsi_open = fetch_rsi(ticker,series_type='open')
    rsi_open_values = result_rsi_open.values

    #fetching rsi low
    result_rsi_low = fetch_rsi(ticker,series_type='low')
    rsi_low_values = result_rsi_low.values

    #fetching rsi high
    result_rsi_high = fetch_rsi(ticker,series_type='high')
    rsi_high_values = result_rsi_high.values

    # calculation rsi ochl4
    # every results have the same number of values and the same timestamps and are already sorted from the most recent timestamp to the longest one
    # simply add each rsi value from each rsi fetch and calculate the mean average

    result_rsi_ochl4 = []
    for x in range(len(rsi_close_values)):
    
        rsi_ohcl = rsi_close_values[x].value + rsi_open_values[x].value +  rsi_low_values[x].value + rsi_high_values[x].value

        rsi_ohcl4 = rsi_ohcl/4.0
        rsi_ohcl4_values = {'timespan':rsi_close_values[x].timestamp, 'value': rsi_ohcl4} 
        
        result_rsi_ochl4.append(rsi_ohcl4_values)

    print ('result_rsi_ochl4',result_rsi_ochl4)
    #return result_rsi_ochl4

# fetch all tickers from polygon api
def fetch_all_tickers():

    client  = get_restclient()

    tickers = []
    for t in client.list_tickers(
        market="crypto",
        active="true", # Specify if the tickers returned should be actively traded on the queried date
        order="asc", # order results ascendant.
        limit="1000", # Limit the number of results returned, default is 100 and max is 1000.
        sort="ticker", # Sort field used for ordering
        ):
        # retrieve ticker, name, active
        ticker_info = {"ticker": t.ticker[2:], #  extract the "X:pair" from the ticker and remove the "X:" to keep only the pair
                        "name":t.name,
                        "active":t.active}
                        #"primary_exchange":t.primary_exchange}
        # store it in the tickers list
        tickers.append(ticker_info)  

    print("A total of",len(tickers), "tickers were fetched.")
    #print("tickers list",  tickers)    
    return tickers

def fetch_rsi_test():

    
   # calculate_rsi_ochl4()
   fetch_all_tickers()

    # import API KEY and URL to fetch cryptos rank
'''    api_key_pol = os.environ['POL_API_KEY']
    print(api_key_pol)

    client = RESTClient(api_key_pol)

    rsi = client.get_rsi(
        ticker="X:BTCUSD",
        timespan="day",
        window="20",
        series_type="open",
        order="desc",
        limit="10",
    )

    print('rsi close',rsi)'''

    





fetch_rsi_test()