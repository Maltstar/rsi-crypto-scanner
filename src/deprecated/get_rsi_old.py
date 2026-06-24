from tradingview_ta import TA_Handler, Interval, Exchange, TradingView
from datetime import datetime
from collections import deque
import time
import csv
import pandas as pd
import argparse
from reduce_screeners_by_ranking import reduce_screeners_by_ranking

# import generic api to clean csv
import little_tools as ll
# define relativ and abs path for the folders "usr", "gen", "db"
import local_api as lapi

import asyncio

start_time = time.time()

def search_symbol(symbol):
    print(TradingView.search("tesla", "america"))


def print_start():
    ## display start time/date

    # datetime object containing current date and time
    # dd/mm/YY H:M:S
    dtbegin_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time begin =", dtbegin_string)

# print the execution time,end date and the number of execptions found
def print_end():
    print ("rsi recording finsihed")
    dtend_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time end =", dtend_string)
    print("execution time in  %s minutes" % ((time.time() - start_time)/60))
    print("have a good day!")

# # parse each crypto symbol in the screener csv file and get the RSI length 14, close
# def record_rsi(csv_screeners):


#     #path to db
#     db_path_f = str(lapi.src_path_db) + "/" + csv_screeners
#     #path to gen
#     gen_path_f = str(lapi.src_path_gen) + "/"

#     ## out file
#     current_date = datetime.now().strftime("%d_%m_%Y")
#     csv_in = csv_screeners.replace('.csv', '') + "-"
#     rsi_out_csv = gen_path_f + "RSI_records" + "-" + csv_in + current_date + "_gen"
#     excp_data = {'exchange':[], 'symbol':[]}
#     rsi_excp_out_csv = gen_path_f + "RSI_exceptions" + "-" + csv_in + current_date + ".csv"


#     with open(db_path_f, 'r') as csv_file:
#         reader = csv.reader(csv_file)
#         print("-> checking rsi for positions in file",db_path_f)
#         ## create new file for rsi records
#         with open(rsi_out_csv+ ".csv", 'w') as csv_file:
#             writer = csv.writer(csv_file)
#             # setting up column of the rsi_out.csv
#             rsi_infoshd = {}
#             rsi_infoshd['description'] = []
#             rsi_infoshd['symbol'] = []
#             rsi_infoshd['RSI 1D: *length: 14 days *source: close)'] = []
#             rsi_infoshd['exchange'] = []
#             rsi_infoshd['date and time'] = []
#             # writing columns labels
#             writer.writerow(rsi_infoshd)
#             count_excp = 0
#             count = 0

#             # skip header line screener,exchange,symbol,desc
#             next(reader)
#             # parsing each line of the csv and calculating rsi
#             for line in reader:
#                 #print(line)
#                 #memorizing the number of position processed
#                 count = count + 1
#                 #getting rsi for current position
#                 # format screener=line[0], sym =line[2], ex=line[1]
#                 Crypto_hdl = TA_Handler(
#                 symbol=line[2],
#                 exchange=line[1],
#                 screener= line[0],
#                 interval=Interval.INTERVAL_1_DAY,
#                 timeout=None
#                 )
#                 try:
#                     analysis= Crypto_hdl.get_analysis()
#                 # if there is an execption, count them and record the position associated
#                 except:
#                     count_excp = count_excp +1
#                     excp_data['exchange'].append(line[1])
#                     excp_data['symbol'].append(line[2])
#                     continue;
#                 else:
#                     if analysis != None:
#                             ##print(analysis)
#                         ##print(count)
#                         ##print(line)
#                         rsi= analysis.indicators["RSI"]
#                         ## update time
#                         t_string = datetime.now().strftime("%H:%M:%S")

#                         ## description/ full name,symbol,RSI, exchange, date and time
#                         rsi_infos = [line[3],line[2],rsi,line[1],t_string]
#                         # recording current rsi calculated in csv file
#                         writer.writerow(rsi_infos)

#                         del analysis
#                         del Crypto_hdl
#                         #if count > 10:
#                         #    break;

#             del writer
#             del reader
#             # converting exception list to dataframe
#             df_excp = pd.DataFrame(excp_data)

#             df_excp.to_csv(rsi_excp_out_csv, encoding='utf-8', index=False)
#             print("number of exceptions:", count_excp)
#             print(" RSI records generated in:",rsi_out_csv)
#             if(count_excp>0):
#                 print(" RSI exceptions generated in:",rsi_excp_out_csv)
#                 print(df_excp)

# parse each crypto symbol and get the RSI length 14, close
#async def record_rsi(rank):
def record_rsi(rank):



    #path to gen
    gen_path_f = str(lapi.src_path_gen) + "/"

    ## out file
    current_date = datetime.now().strftime("%d_%m_%Y_%s")
    #csv_in = csv_screeners.replace('.csv', '') + "-"
    rsi_out_csv = gen_path_f + "RSI_records" + "-"  + current_date + "_gen"
    excp_data = {'exchange':[], 'symbol':[]}
    rsi_excp_out_csv = gen_path_f + "RSI_exceptions" + "-"  + current_date + ".csv"

    crypto_screener_data = reduce_screeners_by_ranking(rank)
    #crypto_screener_data_test = crypto_screener_data#[:]
    crypto_screener_data_test = [[("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)],
      [("BINANCE","BTCUSDT",'',1)],
      [("BINANCE","ETHUSDT",'',2)],
      [("BINANCE","XRPUSDT",'',3)]     
    ]
    screener_type="crypto"


    #with open(db_path_f, 'r') as csv_file:
       # reader = csv.reader(csv_file)
       # print("-> checking rsi for positions in file",db_path_f)
        ## create new file for rsi records
    with open(rsi_out_csv+ ".csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        # setting up column of the rsi_out.csv
        rsi_infoshd = {}
        rsi_infoshd['description'] = []
        rsi_infoshd['symbol'] = []
        rsi_infoshd['RSI 1D: *length: 14 days *source: close)'] = []
        rsi_infoshd['cmc_rank'] = []
        rsi_infoshd['exchange'] = []
        rsi_infoshd['date and time'] = []
        # writing columns labels
        writer.writerow(rsi_infoshd)
        count_excp = 0
        count = 0
        count_analysis_ok = 0

        # skip header line screener,exchange,symbol,desc
        #next(reader)
        # parsing each line of the csv and calculating rsi
        for data in crypto_screener_data_test:
            for element in data:
                print('element' ,element)
               
                
                try:
                    #time.sleep(6)
                    #memorizing the number of position processed
                    count = count + 1
                    #getting rsi for current position
                    # format screener=line[0], sym =line[2], ex=line[1]
                    Crypto_hdl = TA_Handler(
                    symbol=element[1],
                    exchange=element[0],
                    screener= screener_type,
                    interval=Interval.INTERVAL_1_DAY,
                    timeout=None
                    )
                
                    # analysis = await Crypto_hdl.get_analysis()
                    analysis = Crypto_hdl.get_analysis()
                    
                    print('analysis',analysis)
                # if there is an execption, count them and record the position associated
                except Exception as e:
                    print('Error occured:',e)
                    count_excp = count_excp +1
                    print('count_excp',count_excp)
                    excp_data['exchange'].append(element[0])
                    excp_data['symbol'].append(element[1])
                    continue;
                else:
                    if analysis != None:
                            ##print(analysis)
                        ##print(count)
                        ##print(line)
                        count_analysis_ok = count_analysis_ok + 1
                        rsi= analysis.indicators["RSI"]
                        ## update time
                        t_string = datetime.now().strftime("%H:%M:%S")

                        ## description/ full name,symbol,RSI, cmc_rank, exchange, date and time
                        rsi_infos = [element[2],element[1],rsi,element[3],element[0],t_string]
                        # recording current rsi calculated in csv file
                        writer.writerow(rsi_infos)

                        del analysis
                        del Crypto_hdl
                        #if count > 10:
                        #    break;

        del writer
        #del reader
        # converting exception list to dataframe
        df_excp = pd.DataFrame(excp_data)

        df_excp.to_csv(rsi_excp_out_csv, encoding='utf-8', index=False)
        print("number of exceptions:", count_excp)
        print(count," screeners processed :",rsi_out_csv)
        print(count_analysis_ok, " RSI records generated in:",rsi_out_csv)
        if(count_excp>0):
            print(" RSI exceptions generated in:",rsi_excp_out_csv)
            print(df_excp)

#async def start_rsi_records():
def start_rsi_records():
    # display time infos for start
    lapi.print_start()
    # collect RSI for each crypto
    #await record_rsi(1000)
    record_rsi(1000)
    # display time infos for end and execution time and execptions
    lapi.print_end()

# create parser
#parser = argparse.ArgumentParser()

# adding arguments to the parser
# arg[0] :
#    -screeners_list.csv: csv file derivate from the tradingview database with
#                     the following syntax: col[0] labelled 'screener', col[1] 'exchange', col[2] 'symbol'
#
#     Example:         screener,exchange,symbol,desc
#                      crypto,KUCOIN,DENTBTC,Dent / Bitcoin
#                      crypto,BINANCE,NEOUSD,NEO / US Dollar (calculated by TradingView)
#
#    - Note the 4th column is optional only to have an additional information of the current symbol


#parser.add_argument("screeners_list")

# parse the arguments
#args = parser.parse_args()

# get the arguments value
#if args.screeners_list == "":
 #   print ("error, 'screeners_list' csv file parameter missing")
#else:
#    print (" 'args.screeners_list' is", args.screeners_list)
    # display time infos for start
#asyncio.run(start_rsi_records())
start_rsi_records()

#search_symbol('ethereum')
