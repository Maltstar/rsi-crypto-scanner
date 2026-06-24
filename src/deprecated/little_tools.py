import pandas as pd

## removing 1st column 'screener' of csv screener files
# csv_in: file for which a colum has to be removed
# column: name of the column to be removed as a string
def clean_csv(csv_in,column):
    ## removing 1st column of csv screener files
    data_frame = pd.read_csv(csv_in)
    data_frame.pop(column)
    data_frame.to_csv (csv_in, encoding='utf-8', index=False)