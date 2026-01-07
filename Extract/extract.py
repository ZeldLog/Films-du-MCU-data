import pandas as pd

def tsvFileToCsv(tsv_file):
    
    csv_file=tsv_file.replace('.tsv','.csv')
    csv_table=pd.read_csv(tsv_file,sep='\t', dtype = str)
    csv_table.to_csv(csv_file,index=False)

    print("Successfully made csv file")
    return csv_file

## Example

#nconst	primaryName	birthYear	deathYear	primaryProfession	knownForTitles

#nm0000001	Fred Astaire	1899	1987	actor,miscellaneous,producer	tt0072308,tt0050419,tt0027125,tt0025164
#nm0000002	Lauren Bacall	1924	2014	actress,miscellaneous,soundtrack	tt0037382,tt0075213,tt0038355,tt0117057
#nm0000003	Brigitte Bardot	1934	2025	actress,music_department,producer	tt0057345,tt0049189,tt0056404,tt0054452
#nm0000004	John Belushi	1949	1982	actor,writer,music_department	tt0072562,tt0077975,tt0080455,tt0078723


import pandas as pd

def actor_file(table_global, csv_file, chunksize=100_000):

    tconst_set = set(table_global['tconst'])

    result_chunks = []

    for chunk in pd.read_csv(
        csv_file,
        chunksize=chunksize,
        usecols=["nconst", "primaryName", "birthYear", "deathYear",
                 "primaryProfession", "knownForTitles"]
    ):
        chunk['primaryProfession'] = chunk['primaryProfession'].str.split(',')
        chunk = chunk.explode('primaryProfession').rename(
            columns={'primaryProfession': 'profession'}
        )

        chunk = chunk[chunk['profession'].isin(['actor', 'actress'])]
        
        chunk['knownForTitles'] = chunk['knownForTitles'].str.split(',')
        chunk = chunk.explode('knownForTitles').rename(
            columns={'knownForTitles': 'tconst'}
        )

        chunk = chunk[chunk['tconst'].isin(tconst_set)]

        if not chunk.empty:
            result_chunks.append(chunk)
    if result_chunks:
        result = pd.concat(result_chunks, ignore_index=True)
        result.to_csv("./data/actor.csv", index=False)
        return result
    else:
        return pd.DataFrame()
    
    
#tconst	ordering	nconst	category	job	characters

#tt0000001	1	nm1588970	self	\N	["Self"]
#tt0000001	2	nm0005690	director	\N	\N
#tt0000001	3	nm0005690	producer	producer	\N
#tt0000001	4	nm0374658	cinematographer	director of photography	\N

def principal_file(table_global, csv_file, actor_file, chunksize=200_000):

    tconst_set = set(table_global['tconst'])

    result_chunks = []

    for chunk in pd.read_csv(
        csv_file,
        sep='\t',
        chunksize=chunksize,
        usecols=["tconst", "ordering", "nconst", "job",
                 "characters"]
    ):

        chunk = chunk[chunk['tconst'].isin(tconst_set)]

        if not chunk.empty:
            result_chunks.append(chunk)
            
        print(f"Processed chunk with {len(chunk)} relevant rows.")
            
    if result_chunks:
        result = pd.concat(result_chunks, ignore_index=True)
        result.to_csv("./data/actor_2.csv", index=False)
        return result
    else:
        return pd.DataFrame()