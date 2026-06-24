from get_cryptos_by_ranking import reduce_cryptos_to_given_rank
from polygon_api import fetch_all_tickers


# 1- filter tickers per crypto with ranking
# 2- extract a limit number of the tickers for the same crypto
#  

def filter_cryptos(func1,func2,re_pattern,tickers_data, max_exchanges,cmc_rank_symbol):

    matches_nb = 0
   # screener_list_reduced = []
    print('length screeners_data',len(tickers_data))
    print('filter_cryptos 1st ticker',tickers_data[0])

    matched_stablecoin_list = []
    matched_stablecoin_pairs = {}
    # try to match with stablecoins pair
    for data_ticker in tickers_data:
        # extract the "pair" from the data_ticker
        pair = data_ticker['ticker']
       # print('pair',pair)
        # compare it to a symbol
        # compares only if the bumber of screeners matched are less than the max exchanges given
        if matches_nb < max_exchanges/2:
            # record  screener match with symbol
            if func1(re_pattern,pair):
            #if func2(re_pattern,pair):
                matches_nb = matches_nb + 1
                #print('matches_nb',matches_nb)
                new_ticker = data_ticker
                new_ticker['cmc_rank'] = cmc_rank_symbol
                #append screener on list
                matched_stablecoin_list.append(pair)
                yield new_ticker
            #screener_list_reduced.append(new_screener)
        # leave the search loop otherwise
        else: 
            break

    matched_stablecoin_pairs[re_pattern] = matched_stablecoin_list

   # is_not_a_pair_found = any(x == 30 for x in a)

    # if not enough matches with stablecoins take any pair with the crypto symbol aka re_pattern
    if matches_nb < max_exchanges:
        for data_ticker in tickers_data:
            # extract the pair from the data_ticker
            pair = data_ticker['ticker']
         # print('pair',pair)
            # compare it to a symbol
            # compares only if the number of screeners matched are less than the max exchanges given
            if matches_nb < max_exchanges:
                # record  screener match with symbol
                if func2(re_pattern,pair) and not any(x == pair for x in matched_stablecoin_pairs) :
                    matches_nb = matches_nb + 1
                    #print('matches_nb',matches_nb)
                    new_ticker = data_ticker 
                    new_ticker['cmc_rank'] = cmc_rank_symbol
                    #append screener on list
                    yield new_ticker
                 #screener_list_reduced.append(new_screener)
             # leave the search loop otherwise
            else: 
                break



    #return screener_list_reduced

def is_crypto_matched_with_stablecoins(re_pattern,pair):
       # print('tickers_data pair',pair)
       # print('re_pattern',re_pattern)

        patternUSDC = re_pattern + "USDC"
        patternUSDT = re_pattern + "USDT"
        patternDAI = re_pattern + "DAI"

        matched = False

       # look first for standard cyprto pair with stablecoin
       # priority one USDC e.g BTCUSDC
       # USDT e.g BTCUSDT
       # DAI e.g BTCDAI
       # then take every other pair
       # 

        if pair == patternUSDC:
            matched = True
        elif pair == patternUSDT:
            matched = True
        elif pair == patternUSDT:
            matched = True




        return matched
        #return False

def is_crypto_matched(re_pattern,pair):
    return pair.startswith(re_pattern)

# response from trading_view-ta has the following format
# (exchange,pair,description)
# ('CURVE', 'USDCUSDF_72310D', 'USD Coin / Falcon USD on Ethereum (0x72310DAAed61321b02B08A547150c07522c6a976)'),
# ('CURVE', 'WBTCMBTC_95A383.USD', 'Wrapped BTC / Liquid Staked BTC on Ethereum (0x95A3832889B2c3455077991b834efA2d4fA3A945) in USD'), ('CURVE', 'THUSDCRVUSD_9E6411.USD', 'Threshold USD / CurveFi USD Stablecoin on Ethereum (0x9E641187391B7a5fE9ee193359408CA3894f68a2) in USD'), ('CURVE', 'DOLAFXUSD_189B4E.USD', 'Dola USD Stablecoin / fx USD on Ethereum (0x189B4e49B5cAf33565095097b4B960F14032C7D0) in USD'), ('CURVE', 'USDCRLUSD_D001AE', 'USD Coin / RLUSD on Ethereum (0xD001aE433f254283FeCE51d4ACcE8c53263aa186)'), ('CURVE', 'CRVCVXCRV_9D0464.USD', 'Curve DAO Token / Convex CRV on Ethereum (0x9D0464996170c6B9e75eED71c68B99dDEDf279e8) in USD'), ('CURVE', 'SFRXUSDSUSDE_3BD101.USD', 'Staked Frax USD / Staked USDe on Ethereum (0x3BD1017929b43c1414bE2Aca39892590fBa4d6e2) in USD'), ('CURVE', 'CVXCLEVCVX_F9078F', 'Convex Token / CLever CVX on Ethereum (0xF9078Fb962A7D13F55d40d49C8AA6472aBD1A5a6)'), ('CURVE', 'USDECRVUSD_F55B0F.USD', 'USDe / CurveFi USD Stablecoin on Ethereum (0xF55B0f6F2Da5ffDDb104b58a60F2862745960442) in USD'), ('CURVE', 'FRAXUSDE_5DC1BF', 'Frax / USDe on Ethereum (0x5dc1BF6f1e983C0b21EfB003c105133736fA0743)'), ('CURVE', 'ALETHPXETH_30BF3E.USD', 'Alchemix ETH / Pirex Ether on Ethereum (0x30bf3E17CAD0baF1d6B64079Ec219808d2708fEb) in USD'), ('CURVE', 'FRXETHOETH_FA0BBB.USD', 'Frax Ether / Origin Ether on Ethereum (0xfa0BBB0A5815F6648241C9221027b70914dd8949) in USD'),
def match_screeners_with_rank(re_pattern,tickers,max_exchanges,cmc_rank):
    # filerting crypto per symbol and ranking crypto 
    screeeners_filtered_by_rank = list(filter_cryptos(is_crypto_matched_with_stablecoins,is_crypto_matched,re_pattern,tickers,max_exchanges,cmc_rank))
    #print ('screeeners_filtered_by_rank',screeeners_filtered_by_rank)
 #


   # screeeners_filtered_by_rank = filter_cryptos(is_crypto_matched,re_pattern,screeners,max_exchanges,cmc_rank)
    
    return screeeners_filtered_by_rank
    


# filter the tickers fetched by polygon to the reduced cryptos by rank fetched by coinmarketcap 
# crypto: data fetched from coinmarket cap
# tickers: ticker fetched from polygon
# max changes: the number of allowed redundancy for a symbol with a different pair
def filter_screeners_by_ranking(crypto, tickers,max_exchanges):    

    print('crypto',crypto)
    # regular expressions to look for in the screener list containing the crypto symbol
    # any string that contains the crypto symbol
    #re_pattern = "^" + crypto_symbol + ".*$"

    # data from coinmarket cap
    crypto_symbol = crypto['symbol']
    cmc_rank = crypto['cmc_rank']
    re_pattern = crypto_symbol

    # a list of screeners matching the symbol
    reduced_screeners_list = match_screeners_with_rank(re_pattern,tickers,max_exchanges,cmc_rank)
    # removing empty list item from the list
    #reduced_screeners = list(filter(lambda x: len(x) > 0 ,reduced_screeners_list))
    print('reduced_screeners_list',reduced_screeners_list)
    #print('reduced_screeners',reduced_screeners)
    return reduced_screeners_list


def reduce_tickers_by_ranking(rank):

    # full list of screeners from trading-view-ta
    #crypto_screeners = update_crypto_screener()
    crypto_tickers = fetch_all_tickers()

    # list of cryptos from coinmarket cap api reduced below the "rank"
    # format of crypto_by_rank is: ('symbol','rank') e.g (BTC,1)
    cryptos_by_rank = reduce_cryptos_to_given_rank(rank)

    print("crypto_tickers",crypto_tickers[0])

    
    max_exchanges = 3

    # reduce the list of screener crypto to a list of a set of 'max_exchanges' screener per symbol
    reduced_cryptos_with_ranking = [filter_screeners_by_ranking(crypto,crypto_tickers,max_exchanges) for crypto in cryptos_by_rank]
    
    # removing empty list item from the list
    reduced_cryptos_with_ranking_empyty_removed = [tickers for tickers in reduced_cryptos_with_ranking if tickers]
    print('reduced_cryptos_with_ranking_empyty_removed', reduced_cryptos_with_ranking_empyty_removed)

    # sort list according to rank
    # (decorate-sort-undecorate pattern)

    # Python’s Timsort already optimizes, but if the key is costly, you can use the "decorate-sort-undecorate" pattern:
    # Decorate with min cmc_rank
    decorated = [(min(d["cmc_rank"] for d in sublist), sublist) for sublist in reduced_cryptos_with_ranking_empyty_removed]

    # Sort by the precomputed key
    decorated.sort(key=lambda x: x[0])

    # Undecorate
    sorted_cryptos_with_ranking  = [sublist for _, sublist in decorated]

    print('sorted_cryptos_with_ranking', sorted_cryptos_with_ranking)

    return reduced_cryptos_with_ranking

#reduce_screeners_by_ranking(1000)


