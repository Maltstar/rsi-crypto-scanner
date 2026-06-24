from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
from collections import deque
import time
import csv
import pandas as pd
import argparse
import local_api as lapi

# parse each crypto symbol in the screener csv file and get the RSI length 14, close
def check_positions(csv_positions):
    
     #formating path to folder
    #path to position
    usr_path_f = str(lapi.src_path_usr) + "/" + csv_positions
    
    #path to gen
    gen_path_f = str(lapi.src_path_gen) + "/"
    
    #formating generated files name
    current_date = datetime.now().strftime("%d_%m_%Y")
    csv_in = csv_positions.replace('.csv', '') + "-"
    check_pos_out_csv = gen_path_f + "positions_checked" + "-" + csv_in + current_date + "_gen"  + ".csv"
    
    # setup info for exception/error for checking a position
    count_excp = 0
    excp_data = {'exchange':[], 'symbol':[]} 
    check_pos_excp_out_csv = gen_path_f + "positions_checked_excp" + "-" + csv_in + current_date + ".csv"
 
      
    # retrieving positions infos from csv in a dataframe: exchange, symbol, start price, stop price 
    df_pos = pd.read_csv(usr_path_f)
    # list for the current occurence
    l_infos = {'exchange':[],
               'symbol':[],
               'desc':[],
               'start price':[],
               'stop price':[],
               'amount':[],
               'min open price':[],
               'min open price':[],
               '1st stop taken(price)':[],
               'rsi 14 days':[],
               'stop vs open price':[],
               'start vs open price':[],
               'watch position':[],
               'reason to watch':[],
               'sell (sell stop touched)':[]
              }
    # global list, some of all the occurence lists
    l_infos_gl = []
    exchanges = df_pos['exchange'].values.tolist()
    symbols = df_pos['symbol'].values.tolist() 
    start_prices = df_pos['start price'].values.tolist() 
    stop_price = df_pos['stop price'].values.tolist() 
    
   # 
   # csv file column format order is as follow in 'screener','exchange','symbol','desc',    'start price','stop price' ,  
   #                                               row[0],    row[1],   row[2],   row[3],   row[4],        row[5]     ,    
   # csv file column suite: 'min open price', '1st stop taken(price)','amount', 'reason to watch', 'sell (sell stop touched)'
   #                         row[6]         ,      row[7]            ,  row[8] , row[9]          , row[10]
    for index, row in df_pos.iterrows():
        
        # handler used for the rsi of 14 days
        # the class INTERVAL is defined as follow:
        #    INTERVAL_1_MINUTE = "1m"
        #    INTERVAL_5_MINUTES = "5m"
        #    INTERVAL_15_MINUTES = "15m"
        #    INTERVAL_1_HOUR = "1h"
        #    INTERVAL_4_HOURS = "4h"
        #    INTERVAL_1_DAY = "1d"
        #    INTERVAL_1_WEEK = "1W"
        #    INTERVAL_1_MONTH = "1M"
        
        
        Crypto_hdl = TA_Handler(
                symbol=row[2],
                exchange=row[1],
                screener= row[0],
                interval=Interval.INTERVAL_1_DAY,
                timeout=None
                )
        
        # handler used for an accurate price 1 minute
        Crypto_hdl_min = TA_Handler(
                symbol=row[2],
                exchange=row[1],
                screener= row[0],
                interval=Interval.INTERVAL_1_MINUTE,
                timeout=None
                )
        
        
        try: 
            analysis_day= Crypto_hdl.get_analysis()
            analysis_min= Crypto_hdl_min.get_analysis()
           
        except:  # if there is any execption, count them and record the position associated    
            count_excp = count_excp +1
            excp_data['exchange'].append(row[1])
            excp_data['symbol'].append(row[2])
            # instanciating l_infos with dummy values for analysis, needed to make the size of the list index and dataframe index match
            l_infos['exchange'].append(row[1])
            l_infos['symbol'].append(row[2])
            l_infos['desc'].append(row[3])
            l_infos['start price'].append(row[4])
            l_infos['stop price'].append(row[5])
          #  l_infos['1st stop taken(price)'].append(row[7])
            l_infos['amount'].append(row[8])
            l_infos['reason to watch'].append(row[9])
            l_infos['sell (sell stop touched)'].append(row[10])
            l_infos['min open price'].append("0$")
            l_infos['rsi 14 days'].append("0")
            l_infos['stop vs open price'].append("0")
            l_infos['start vs open price'].append("0")
            l_infos['watch position'].append("manually")
            continue;
            
        else: 
            if (analysis_day != None) and (analysis_min != None) :  # otherwise the analysis were successfully retrieved, all good, proceeding... :
            
            #rsi = analysis.indicators["RSI"]
            #current_open_price = analysis.indicators["open"]
            #current_close_price = analysis.indicators["close"]
            # update time
            # recording all infos in a list of list
                t_string = datetime.now().strftime("%H:%M:%S")
                l_infos['exchange'].append(row[1])
                l_infos['symbol'].append(row[2])
                l_infos['desc'].append(row[3])
                l_infos['start price'].append(row[4])
                l_infos['stop price'].append(row[5])
              #  l_infos['1st stop taken (price)'].append(row[7])
                l_infos['amount'].append(row[8])
                l_infos['reason to watch'].append(row[9])
                l_infos['min open price'].append((analysis_min.indicators["open"]))
                l_infos['rsi 14 days'].append(analysis_day.indicators["RSI"])
                
                
                
                # calculating:
                # - stop price against open/close price 
                # - start price against open/close price
                
                # remove '$' and ',' to convert price from string to float
                start_price = str(row[4])
                stop_price = str(row[5])
                
                start_price = start_price.replace('$', '')
                start_price = start_price.replace(',', '')
                stop_price = stop_price.replace('$', '')
                stop_price = stop_price.replace(',', '')
                
                start_price_f = float(start_price)
                stop_price_f = float(stop_price)
                
                
                
                # calculating:
                stop_price_vs_open_price = stop_price_f - float(analysis_min.indicators["open"])
                start_price_vs_open_price = start_price_f - float(analysis_min.indicators["open"])
                
                # calculating in percentage, adding the multiplication * -1, to know if the asset is upper oder under current price
                # a positive result means that the current price is above the stop
                # a negative result means that the current price is still below the stop
                
                stop_price_vs_open_price_p = (stop_price_vs_open_price/stop_price_f)*(-100)
                start_price_vs_open_price_p = (start_price_vs_open_price/start_price_f)*(-100)
                
                
                #l_infos['stop vs open price'].append(str(stop_price_vs_open_price))
                #l_infos['stop vs close price'].append(str(stop_price_vs_close_price))
                #l_infos['start vs open price'].append(str(start_price_vs_open_price))
                #l_infos['start vs close price'].append(str(start_price_vs_close_price))
                
                
                l_infos['stop vs open price'].append(str(stop_price_vs_open_price_p))
                l_infos['start vs open price'].append(str(start_price_vs_open_price_p))
                
               # print(l_infos['reason to watch'][index])
                # for the positions which were not sold at all
                # if the current position price is greater than the stop price then the position must be watched otherwise don t care for now
                #the position of the current row was not sold at all
                if ((l_infos['reason to watch'][index].__contains__("1st")) == True ):
                    if  (stop_price_vs_open_price_p>0):
                        l_infos['watch position'].append("yes")
                    else:
                        l_infos['watch position'].append("no")
                    # in the case of the position which were not sold at all, the sell stop is irrelevant     
                    l_infos['sell (sell stop touched)'].append("no")    
                     #print("contains 1st")
                     #print(l_infos['symbol'][index])
                     #print( l_infos['watch position'][index])
                else: #the positions were sold partially
                    l_infos['watch position'].append("yes")
                     #print("contains 2nd")
                     #print(l_infos['symbol'][index])
                     #print( l_infos['watch position'][index])
                    if (stop_price_vs_open_price_p>0): #the position is still above the sell stop 
                        l_infos['sell (sell stop touched)'].append("no")
                    else: #the position is belpw or equal to the sell stop 
                        l_infos['sell (sell stop touched)'].append("yes")
                                       
                
                del analysis_day
                del analysis_min
                del Crypto_hdl
                del Crypto_hdl_min
     #   break;
           
    print(l_infos)
    print(df_pos)
    #   the position order of the column comes from the template of the file read csv_positions, then adding a new column will add it after the last existing column
    df_pos['start price'] = l_infos['start price']
    df_pos['stop price'] = l_infos['stop price']
 #   df_pos['1st stop taken (price)'] = l_infos['1st stop taken (price)']
    df_pos['reason to watch']= l_infos['reason to watch']
    df_pos['sell (sell stop touched)']= l_infos['sell (sell stop touched)']
    df_pos['watch position'] = l_infos['watch position']
    df_pos['min open price'] = l_infos['min open price']
    df_pos['rsi 14 days'] = l_infos['rsi 14 days']
    df_pos['stop vs open price'] = l_infos['stop vs open price']
    df_pos['start vs open price'] = l_infos['start vs open price']


    # converting exception list to dataframe
    df_excp = pd.DataFrame(excp_data)
   


    df_excp.to_csv(check_pos_excp_out_csv, encoding='utf-8', index=False)
    df_pos.to_csv(check_pos_out_csv, encoding='utf-8', index=False)
    
    print("number of exceptions:", count_excp)
    print(" position_checked generated in:",check_pos_out_csv)
    if(count_excp>0):
        print(" RSI exceptions generated in:",check_pos_excp_out_csv)
        print(df_excp)
                
def start_check_positions(csv_pos_list):
    # display time infos for start            
    lapi.print_start()
    # check position
    check_positions(csv_pos_list)
    # display time infos for end and execution time and execptions 
    lapi.print_end()

# create parser
parser = argparse.ArgumentParser()

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


parser.add_argument("pos_list")
 
# parse the arguments
args = parser.parse_args()
 
# get the arguments value
if args.pos_list == "":
    print ("error, 'pos_list' csv file parameter missing")
else:
    print (" 'args.screeners_list' is", args.pos_list)
    # display time infos for start            
    start_check_positions(args.pos_list)
