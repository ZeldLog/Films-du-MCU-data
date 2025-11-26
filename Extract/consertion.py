import pandas as pd

def tsvFileToCsv():
    tsv_file='data.tsv'

    # reading given tsv file
    csv_table=pd.read_table(tsv_file,sep='\t')

    csv_table.to_csv('data.csv',index=False)

    print("Successfully made csv file")