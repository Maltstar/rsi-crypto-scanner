import pandas as pd
import re
from typing import Pattern
# define relativ and abs path for the folders "usr", "gen", "db"
import local_api as lapi
import argparse
from datetime import datetime

# extract crypto symbol name from LiveCoinWatch listing
# symbol are listed with their full name in one cell
# removing the name of the cryptos and keeping only the symbol

def extract_symbol_from_LWC(listing):
    
    #path to position
    usr_path_f = str(lapi.src_path_usr) + "/" + listing

    symbol = ""
    string = ""
    df_pos_desc = pd.read_csv(usr_path_f)
    df_coin = df_pos_desc['Coin'].values.tolist()
    l_symbol = {'symbol':[]}
    
    # formating generated files
    out_file_prefix = "_symbols_extracted_"
    out_file_suffix = "_gen.csv"
    current_date = datetime.now().strftime("%d_%m_%Y")
    #path to gen
    gen_path_f = str(lapi.src_path_gen) + "/" 

    # for each position, search the associated screener in the trading view database (csv)
        #for pos_desc in df_pos_desc:

         # listing is given as follow <Symbol><Full cryptoname>, 
         # the syntax of the elements is as follow <Full cryptoname> is as follow (syntax1) <single Uppercase> < several lowercase>, also (syntax2) <several Uppercase> in this case the name of the symbol is duplicated 
         # within a string (example "ZEUZZEUZ"), another pattern is (syntax3) is <several Uppercase><severallowercases>, example "SparkSparkpoint", the last pattern (syntax4) <several Uppercase> <space> <several lowercase>,
         # example(BTSEBTSE Token)
         # , in this case the content of <several Uppercase> is the symbol name duplicated, another partern   :
         # * so for syntax1 looking for the pattern  <1 Uppercase> <several lower cases> <any character 0 or several times> <end of the string> and removing it from the string
         # * so for syntax2 looking for <several Uppercase> <end of the string> then spliting the result string in half
         # * so for syntax3 looking manually as there is no way to automate the research of the symbol name over the string
         # * so for syntax4 looking for <several Uppercase> <whitespace> <any character 0 or several times> <end of the string> followed by a space then removing the space from the result and spliting the rest of the result string into 2 equal part

            # any string that contains the position name
    re_pattern_syx1 = r'[A-Z0-9]{1}[a-z0-9]{1,}.*$'
    re_pattern_syx2 = r'^\s*[A-Z0-9]{2,}$'
    #re_pattern_syx4 = r'[A-Z0-9]{1,}\s.*$'
    re_pattern_syx4 = r'[A-Z0-9]{1,}\s'

    for element in df_coin:
        # testing the string configuration:
        # test syntax 4
        res = re.search(re_pattern_syx4,element)
        if (bool(res) == True):
            print("syntax4 value found in reg",res.group())
            string = str(res.group())
            string = string.replace(' ', '')
            symbol = string[:len(string)//2]
            print("syntax4",symbol)            
        else: # test syntax 2
                res = re.search(re_pattern_syx2,element)
                if (bool(res) == True): # splitting string in two equal parts 
                    #string = str(x.group())
                    string = str(res.group())
                    string2 = string.replace(' ','') # removing space
                    print("syntax2 value found in reg",res.group())
                    if(len(string2)%2 == 0): # splitting string in two equal parts if the number of characters is pair
                        symbol = string2[:len(string2)//2]
                    else:
                        symbol = string2 # otherwise copying and looking manually for the symbol later on
                    print("syntax2",symbol)
                else: # test syntax 1 
                    res = re.search(re_pattern_syx1,element) 
                    if (bool(res) == True): # removing space, then splitting string in two equal parts 
                        print("syntax1 value found in reg",res.group())
                        symbol = element.replace(str(res.group()),'')
                        symbol = symbol.replace(' ', '') # removing space
                        print("syntax1",symbol)
                    else: # syntax 3 is confirmed, copying the whole string and looking manually to find the symbol
                        symbol = element
                        print("syntax3",symbol)

        # storing the symbol found
        l_symbol['symbol'].append(symbol)

     # formating output files
    out_file = gen_path_f + listing.replace('.csv', '') + out_file_prefix + current_date + out_file_suffix
    
    #converting symbol list into csv file    
    df_symbol = pd.DataFrame(l_symbol) 
    df_symbol.to_csv(out_file, encoding='utf-8', index=False)
    print(df_symbol)
    print("symbols for submitted list generated in file:",out_file)


# extract crypto symbol name from CoinMarketcap listing
# symbol are listed with their full name in one cell
# removing the name of the cryptos and keeping only the symbol

def extract_symbol_from_CMCAP(listing):
    
    #path to position
    usr_path_f = str(lapi.src_path_usr) + "/" + listing

    symbol = ""
    string = ""
    df_pos_desc = pd.read_csv(usr_path_f)
    df_coin = df_pos_desc['Name'].values.tolist()
    l_symbol = {'symbol':[]}
    
    # formating generated files
    out_file_prefix = "_symbols_extracted_"
    out_file_suffix = "_gen.csv"
    current_date = datetime.now().strftime("%d_%m_%Y")
    #path to gen
    gen_path_f = str(lapi.src_path_gen) + "/" 

    # for each position, search the associated screener in the trading view database (csv)
        #for pos_desc in df_pos_desc:

         # listing is given as follow <Full cryptoname><Symbol>, 
         # the syntax of the elements is as follow <Full cryptoname> is as follow:
         # (syntax1) <single Uppercase> < several lowercase> <optional number>  or even space character, or sometime 2 words with upper case also  ex: AlienWorldsTLM or Thezos2XTZ or "Axie Infinity3AXS" or FIO ProtocolFIO
         # , also (syntax2) <several Uppercase> in this case the name of the symbol is duplicated  ex:NFTXNFTX, there are some cases where the name of the crypto and the symbol are all in
        #  uppercase and it is not possible to find the name easily example CUMROCKETCUMMIES
         # another pattern is (syntax3) is <several Uppercase> <single lowercase>, example "BLOCKvVEE", 
         # * so for syntax1 looking for the pattern  <1 Uppercase> <several lower cases or several times>  or 
         # <1 Uppercase> <several lower cases> <a number 1 or several times> <end of the string> and removing it from the string
        
         # * so for syntax2 looking for <several Uppercase> <end of the string> then spliting the result string in half
         # * so for syntax4 looking for <several Uppercase> <lowercase or number 1 or several times> or then removing pattern found

            # any string that contains the position name
    re_pattern_syx1 = r'[A-Z0-9]{1}[a-z0-9]{1,}'
    re_pattern_syx2 = r'^[A-Z0-9]{2,}$'
    re_pattern_syx3 = r'^[A-Za-z0-9]{2,}[.]{1,}[a-z]{1,}$' #example for FUD.financeFUD or pulltherug.financeRUGZ
    #re_pattern_syx4 = r'[A-Z0-9]{1,}\s.*$'
    re_pattern_syx4 = r'[A-Z0-9]{2,}[a-z0-9]{1,}'
    
    # any set of uppercase until end of the string
    re_pattern = r'[A-Z]{2,}$'
    re_pattern_with_minus = r'[A-Z]{1,}[-]+[A-Z0-9]{1,}$' #example for Cubiex Power CBIX-P
    
    # any set of lowercase until end of the string for the exceptions, ex: for LUKSO and ERC20ERC20, the symbol ends with a lower case LYXe, so far this is the only exception
    re_pattern_excp_lc = r'[a-z]{1,}$'
    re_pattern_excp_nb = r'[0-9]{1,}$'
    
    for element in df_coin:
        # testing the string configuration:

        
        res_syx1 = re.search(re_pattern_syx1,element)
        res_syx4 = re.search(re_pattern_syx4,element)
        res_syx3 = re.search(re_pattern_syx3,element)
        res_syx_mns = re.search(re_pattern_with_minus,element)
        res_excp_lc = re.search(re_pattern_excp_lc,element)
        res_excp_nb = re.search(re_pattern_excp_nb,element)
        
        if (bool(res_syx1)):
            print("syx1",str(res_syx1.group()))
        if (bool(res_syx4)):
            print("syx4",str(res_syx4.group()))
        
        # filtering the pattern for syntax 1
        if ( (bool(res_syx1) or bool(res_syx4) or bool(res_syx4) == True or bool(res_syx3) == True) and ( bool(res_excp_lc) == False and bool(res_excp_nb) == False) ):
            if (bool(res_syx_mns) == True):  # filtering the symbol containing a minus
                symbol = str(res_syx_mns.group())
            else: # applying common extract for re_pattern
                res = re.search(re_pattern,element)
                symbol = str(res.group())
        else:
            res_syx2 = re.search(re_pattern_syx2,element)
            if(bool(res_syx2) == True):
                string = str(res_syx2.group())
                if(len(string)%2 == 0): # splitting string in two equal parts if the number of characters is pair
                    symbol = string[:len(string)//2]
                else:
                    symbol = element
            else: # new syntax not yet encountered
                print("unknown syntax for",element) 
                symbol = element
                
        print(symbol)    
         # test syntax 4           
        #res = re.search(re_pattern_syx4,element)
        #if (bool(res) == True):
        #    print("syntax4 value found in reg",res.group())
        #    symbol = element.replace(str(res.group()),'')
        #    print("syntax4",symbol)            
        #else: # test syntax 2
        #        res = re.search(re_pattern_syx2,element)
        #        if (bool(res) == True):
        #            #string = str(x.group())
        #            string = str(res.group())
        #            print("syntax2 value found in reg",res.group())
        #            if(len(string)%2 == 0): # splitting string in two equal parts if the number of characters is pair
        #                symbol = string[:len(string)//2]
        #            else:
        #                symbol = element # otherwise copying and looking manually for the symbol later on
        #            print("syntax2",symbol)
        #        else: # test syntax 1 
        #            res = re.search(re_pattern_syx1,element) 
        #            if (bool(res) == True):
        #                if " " in element:# if there is a space character it means that we have to remove 2 times the pattern at there are 2 words ex: "Axie Infinity3AXS"
        #                    element = element.replace(" ",'')
        #                    print("syntax1 value found in reg",res.group())
        #                    symbol = element.replace(str(res.group()),'') # removing 1st word
        #                    print("syntax1 rest of string after 1st remove",symbol)
        #                    if(re.search(re_pattern_syx2,symbol) ): # splitting the 2nd word in 2 equal parts
        #                        symbol = symbol[:len(symbol)//2]
        #                    else:  # otherwise removing the 2nd word 
        #                        res = re.search(re_pattern_syx1,symbol) 
        #                        print("syntax1 rest of string after 1st remove res.group",res.group())
        #                        symbol = symbol.replace(str(res.group()),'') # removing 2nd word
        #                        # as it may happen that there are 3 words looking for another existing word
        #                        res = re.search(re_pattern_syx1,symbol) 
        #                        if bool(res):  # a 3rd word is comfirmed so removing it
        #                            symbol = symbol.replace(str(res.group()),'') # removing 2nd word 
        #                else: #otherwise only the 1st word
        #                    symbol = element.replace(str(res.group()),'') # removing 1st word
        #                print("syntax1",symbol)
        #            else: # other syntax confirmed, copying the whole string and looking manually to find the symbol
        #                symbol = element
        #                print("syntax3",symbol)

        # storing the symbol found
        l_symbol['symbol'].append(symbol)

     # formating output files
    out_file = gen_path_f + listing.replace('.csv', '') + out_file_prefix + current_date + out_file_suffix
    
    #converting symbol list into csv file    
    df_symbol = pd.DataFrame(l_symbol) 
    df_symbol.to_csv(out_file, encoding='utf-8', index=False)
    print(df_symbol)
    print("symbols for submitted list generated in file:",out_file)
    
    
    
def start_extract_symbol(listing):

    
    lapi.print_start()  
    if "LCW" in listing: #liveCoinWatch listing recognized 
        extract_symbol_from_LWC(listing)
    else:
        if "CMCAP" in listing: #CoinMarketCap listing recognized 
            extract_symbol_from_CMCAP(listing)
        else:
            print("file syntax type unknown")
            print("only listing from coinmarketcap and livecoinwatch supported")     
    lapi.print_end()



# create parser
parser = argparse.ArgumentParser()

# adding arguments to the parser
# arg[0] : 
#    -LWC_Coin_list.csv: csv file listing the crypto with the following syntax on the column "Coin" <Symbol><full crypto name>
#
#     Example:         screener,exchange,symbol,desc
#                      crypto,KUCOIN,DENTBTC,Dent / Bitcoin
#                      crypto,BINANCE,NEOUSD,NEO / US Dollar (calculated by TradingView)
#
#    - Note the 4th column is optional only to have an additional information of the current symbol


parser.add_argument("LWC_Coin_list")
 
# parse the arguments
args = parser.parse_args()
 
# get the arguments value
if args.LWC_Coin_list == "":
    print ("error, 'LWC_Coin_list' csv file parameter missing")
else:
    print (" 'args.LWC_Coin_list' is", args.LWC_Coin_list)
    # display time infos for start            
    start_extract_symbol(args.LWC_Coin_list)