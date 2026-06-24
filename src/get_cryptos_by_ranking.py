from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv


def get_cryptos_with_ranking():

  cryptos_with_ranking = fetch_cryptos_with_ranking()
  #sort according to ranking
  sorted_cryptos_with_ranking= sorted(cryptos_with_ranking, key=lambda k: k["cmc_rank"])
  return sorted_cryptos_with_ranking
  #print(sorted_cryptos_with_ranking[0])
  #print(sorted_cryptos_with_ranking[1])

def is_cmc_higher_or_equal(data,rank):
  return data <= rank

# extract only the necessary data:
# 'name','symbol','cmc_rank'
def reduce_cypto_data(data):


  crypto_data_reduced = {}
 # crypto_data_reduced['name'] = data['name']
  crypto_data_reduced['symbol'] = data['symbol']
  crypto_data_reduced['cmc_rank'] = data['cmc_rank']

  #print('crypto_data_reduced',crypto_data_reduced)

  return crypto_data_reduced


# 1- fetch

def reduce_cryptos_to_given_rank(rank):

  cryptos = get_cryptos_with_ranking()
  #cryptos_filtered = list(filter(lambda x: reduce_cypto_data(x, rank), cryptos))

  cryptos_filtered = list(filter(lambda x: is_cmc_higher_or_equal(x['cmc_rank'], rank), cryptos))
  # filtering only the crypto having a rank lower than the given one 
  sorted_cryptos_with_ranking= sorted(cryptos_filtered, key=lambda k: k["cmc_rank"])
  # extracting only the necessary data from the sorted cryptos
  reduced_cryptos_with_ranking = [reduce_cypto_data(x) for x in sorted_cryptos_with_ranking]
  print('cryptos reduced to rank ',len(reduced_cryptos_with_ranking))

  return reduced_cryptos_with_ranking
"""   print('reduced_cryptos_with_ranking length',len(reduced_cryptos_with_ranking))
  print(reduced_cryptos_with_ranking[0])
  print(reduced_cryptos_with_ranking[1]) """




# request all active cryptocurrencies with latest market data from coinmarketcap
def fetch_cryptos_with_ranking():
  # Load environment variables from .env file
  load_dotenv()

  # import API KEY and URL to fetch cryptos rank
  api_key_cmc = os.environ['CMC_PRO_API_KEY']
  url = os.environ['CMC_PRO_URL']
  #cryptos_with_ranking = []

  # setup request as a session with different settings
  # doc https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyListingsLatest
  parameters = {
    'start':'1', # ooffset the start (1-based index) of the paginated list of items to return
    'limit':'5000', # number of results
    'convert':'USD' # calculate market quotes in a specific currency
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key_cmc,
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    cryptos_data_cmc_ranking = data['data']
    #key_data = data.keys()
    #print(key_data)
    return cryptos_data_cmc_ranking
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


# reduce all resutls to cryptos matching the range of the given rank
cryptos_ranked = reduce_cryptos_to_given_rank(1000)

print('reduced_cryptos_with_ranking length',len(cryptos_ranked))
print(cryptos_ranked[0])
print(cryptos_ranked[1])
