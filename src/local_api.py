import pandas as pd

from pathlib import Path
from datetime import datetime
import time

# *********************************************
# * DEFNITION of path for input and output folders
# *********************************************
# formatting path for input and output folders 
# `cwd`: current directory is straightforward
cwd = Path.cwd()
mod_path = Path(__file__).parent


rel_path_db = '../db/'
rel_path_gen = '../gen/'
#rel_path_gen_lst = '../../gen/listing'
rel_path_usr = '../usr/'
#rel_path_usr_lst = '../../usr/listing'
src_path_db = (mod_path / rel_path_db).resolve()
src_path_gen = (mod_path / rel_path_gen).resolve()
src_path_usr = (mod_path / rel_path_usr).resolve()
#src_path_lst = (mod_path / rel_path_lst).resolve()

start_time = time.time()
    
def print_start():
    ## display start time/date
   
    # datetime object containing current date and time
    # dd/mm/YY H:M:S
    dtbegin_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time begin =", dtbegin_string)
    print(" ")
    print ("execution in progress...")
    print(" ")

# print the execution time,end date and the number of execptions found    
def print_end():
    print(" ")
    print ("execution finsihed :)")
    print(" ")
    dtend_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time end =", dtend_string)
    print("execution time in  %s minutes" % ((time.time() - start_time)/60))
    print("have a good day!")

## removing 1st column 'screener' of csv screener files
# csv_in: file for which a colum has to be removed
# column: name of the column to be removed as a string
def clean_csv(csv_in,column):
    ## removing 1st column of csv screener files
    data_frame = pd.read_csv(csv_in)
    data_frame.pop(column)
    data_frame.to_csv (csv_in, encoding='utf-8', index=False)