import pandas as pd

def tsvFileToCsv(tsv_file):
    
    csv_file=tsv_file.replace('.tsv','.csv')
    csv_table=pd.read_csv(tsv_file,sep='\t', dtype = str)
    csv_table.to_csv(csv_file,index=False)

    print("Successfully made csv file")
    return csv_file
    
#tconst	ordering	nconst	category	job	characters

#tt0000001	1	nm1588970	self	\N	["Self"]
#tt0000001	2	nm0005690	director	\N	\N
#tt0000001	3	nm0005690	producer	producer	\N
#tt0000001	4	nm0374658	cinematographer	director of photography	\N

def principal_file(table_global, tsv_file, top=10, chunksize=200_000):

    tconst_set = set(table_global['tconst'])

    result_chunks = []

    for chunk in pd.read_csv(
        tsv_file,
        sep='\t',
        chunksize=chunksize,
        usecols=["tconst", "ordering", "nconst",
                 "characters"]
    ):

        chunk = chunk[chunk['tconst'].isin(tconst_set)]

        if not chunk.empty:
            result_chunks.append(chunk)
    
    print("Successfully extracted principal file data")   
    if result_chunks:
        result = pd.concat(result_chunks, ignore_index=True)
        return result.query('ordering <= @top')
    else:
        return pd.DataFrame()
    
    

#nconst	primaryName	birthYear	deathYear	primaryProfession	knownForTitles

#nm0000001	Fred Astaire	1899	1987	actor,miscellaneous,producer	tt0072308,tt0050419,tt0027125,tt0025164
#nm0000002	Lauren Bacall	1924	2014	actress,miscellaneous,soundtrack	tt0037382,tt0075213,tt0038355,tt0117057
#nm0000003	Brigitte Bardot	1934	2025	actress,music_department,producer	tt0057345,tt0049189,tt0056404,tt0054452
#nm0000004	John Belushi	1949	1982	actor,writer,music_department	tt0072562,tt0077975,tt0080455,tt0078723


def actor_file(table_principal,name_file,file_principal, chunksize=100_000):

    tconst_set = set(table_principal['tconst'])

    table_principal = principal_file(table_principal,file_principal)
    
    nconst_set = set(table_principal['nconst'])

    result_chunks = []
    

    for chunk in pd.read_csv(
        name_file,
        chunksize=chunksize,
        usecols=["nconst", "primaryName", "knownForTitles"]
    ):

        chunk = chunk[chunk['nconst'].isin(nconst_set)]

        if not chunk.empty:
            result_chunks.append(chunk)

    print("Successfully extracted name file data")  
    if result_chunks:
        result = pd.concat(result_chunks, ignore_index=True)
        result.to_csv("./data/name.csv", index=False)
        return result
    else:
        return pd.DataFrame()
    
    
#tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres

#tt0000001	short	Carmencita	Carmencita	0	1894	\N	1	Documentary,Short
#tt0000002	short	Le clown et ses chiens	Le clown et ses chiens	0	1892	\N	5	Animation,Short
#tt0000003	short	Poor Pierrot	Pauvre Pierrot	0	1892	\N	5	Animation,Comedy,Romance
#tt0000004	short	Un bon bock	Un bon bock	0	1892	\N	12	Animation,Short
#tt0000005	short	Blacksmith Scene	Blacksmith Scene	0	1893	\N	1	Short
#tt000006	short Chinese Opium Den Chinese Opium Den  1  Short
    
    
def all_movie_table(file_title_basic, chunksize=200_000):
    result_chunks = []
    
    titleType_set = set(["tvSeries", "movie","tvMiniSeries"])

    for chunk in pd.read_csv(
        file_title_basic,
        chunksize=chunksize,
        usecols=["tconst", "titleType", "primaryTitle","startYear","runtimeMinutes"]
    ):

        chunk = chunk[chunk['titleType'].isin(titleType_set)]

        if not chunk.empty:
            result_chunks.append(chunk)

    print("Successfully extracted all movie/series file data")  
    if result_chunks:
        result = pd.concat(result_chunks, ignore_index=True)
        result.to_csv("./data/film.csv", index=False)
        return result
    else:
        return pd.DataFrame()