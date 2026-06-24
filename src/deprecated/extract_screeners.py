#!/usr/bin/python
## extract_screeners.py (positions)

import sys, getopt
import argparse
import csv
import pandas as pd
from datetime import datetime

# import generic api to clean csv
import little_tools as ll

import numpy as np

# define relativ and abs path for the folders "usr", "gen", "db"
import local_api as lapi


# extract screener from csv file exported from trading view database and copy them into a csv file
def extract_screener_from_positions(csv_db_screeners, csv_positions):

    # formating generated files
    out_file_prefix = "_scrn_ex_sym_"
    excp_file_prefix = "_excp"
    out_file_suffix = "_gen.csv"
    
    current_date = datetime.now().strftime("%d_%m_%Y")

    df_symex = pd.DataFrame()
    df_symexdesc = pd.DataFrame()
    df_excp = pd.DataFrame()
    l_excp = {'symbol':[]}
    cnt_excp = 0
    cnt_ok = 0
    
    #path to position
    usr_path_f = str(lapi.src_path_usr) + "/" + csv_positions
    #path to db
    db_path_f = str(lapi.src_path_db) + "/" + csv_db_screeners
    #path to gen
    gen_path_f = str(lapi.src_path_gen) + "/" 
    
    # retrieve positions from csv as a string array 
    df_pos = pd.read_csv(usr_path_f)
    screener = df_pos['symbol'].values.tolist()
    # opening csv file exported from trading view database
    df = pd.read_csv(db_path_f)
    # initialize flag for a symbol match in the database
    symb_found = False
    
    # for each position, search the associated screener in the trading view database (csv)
    for position in screener:

        # regular expressions to look for in the screener list containing the position name
        # any string that contains the position name
        re_pattern = "^" + position + ".*$"
        
        # checking on the csv file the column "symbol" for all the strings which contains the name of the position and
        # extracting the associated row
        
        # checking on the csv file the column "symbol" for all the strings which contains the name of the position and
        # extracting the indexes of True or false for each match and looking for a match true 
        match_res = df['symbol'].str.contains(re_pattern,regex=True).to_list()
        for match in match_res:
            if(match == True):
                symb_found = True
                break
            else:
                symb_found = False

        # if the reg pattern is found adding it to the list        
        if(symb_found == True): 
            # checking on the csv file the column "symbol" for all the strings which contains the name of the position and
            # extracting the associated row
            mask = np.column_stack([df['symbol'].str.contains(re_pattern,regex=True)]) 
            df_symexdesc = df_symexdesc.append(df.loc[mask.any(axis=1)])
            # update count found positions
            cnt_ok = cnt_ok + 1 
        # otherwise adding it to the exception and print it at the end   
        else: 
            cnt_excp = cnt_excp + 1
            l_excp['symbol'].append(position)
        
    df_excp['symbol'] = l_excp['symbol']
    
    # formating output files
    out_file = gen_path_f + csv_positions.replace('.csv', '') + out_file_prefix + current_date + out_file_suffix
    excp_file = gen_path_f + csv_positions.replace('.csv', '') + out_file_prefix + current_date + excp_file_prefix + out_file_suffix
    
    #converting dataframe with screeners customized positions into a csv 
    df_symexdesc.to_csv(out_file, encoding='utf-8', index=False)
    df_excp.to_csv(excp_file, encoding='utf-8', index=False)
    #removing default column "screener (contains always keyword "crypto")
    #ll.clean_csv(out_file,"screener")
    print("screeners for submitted positions generated in file:",out_file)
    print("number of positions found in trading view database:",cnt_ok)
    if(cnt_excp>0):
        print("number of positions not found in trading view database:", cnt_excp)
        print("the following positions were not found:")
        print(df_excp['symbol'])

def start_extract_screeners(db_screeners, positions_list ):
    lapi.print_start()
    extract_screener_from_positions (db_screeners,positions_list)
    lapi.print_end()
    
    
# create parser
parser = argparse.ArgumentParser()

# adding arguments to the parser
# arg[0] : 
#    -db_screeners: csv file of the tradingview database screeners
# arg[1] :
#    -positions_list: csv file of the positions to be checked for screeners for

parser.add_argument("db_screeners")
parser.add_argument("positions_list")
 
# parse the arguments
args = parser.parse_args()
 
# get the arguments value
if args.db_screeners == "":
    print ("error, 'db_screeners' csv file parameter missing")
else:
    print (" 'args.db_screeners' is", args.db_screeners)
    print ("'args.db_screeners' is", args.positions_list)
    start_extract_screeners(args.db_screeners,args.positions_list )

# to add the usage description
# syntax to call the script extract_screeners.py <csv file extracted from tradingview database> <csv file with positions symbol>
# ex: extract_screeners crypto_screeners.csv positions.csv