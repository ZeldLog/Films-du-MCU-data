import pandas as pd

def tsvFileToCsv(tsv_file):
    
    csv_file=tsv_file.replace('.tsv','.csv')
    csv_table=pd.read_table(tsv_file,sep='\t')
    csv_table.to_csv(csv_file,index=False)

    print("Successfully made csv file")
    return csv_file