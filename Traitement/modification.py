import pandas as pd

def removeData(table,column_name,data_to_remove):
    table=table[table[column_name]!=data_to_remove]
    print(f"Successfully removed {data_to_remove} from {column_name}")
    return table
    
def removeColumn(table,column_name):
    table=table.drop(column_name,axis=1)
    print(f"Successfully removed {column_name} column")
    return table
    
    
def addcolumn(file,column_name,default_value):
    table=pd.read_csv(file)
    table[column_name]=default_value
    table.to_csv(file,index=False)
    print(f"Successfully added column {column_name} with default value {default_value}")
    
    
#### Deprecated   
#def add_tconst(file_basics,table):
#    imdb = pd.read_csv(file_basics,sep='\t', dtype = str)
#   table['year'] = table['release_date'].str[:4]
#    merged = table.merge(
#        imdb[['tconst', 'primaryTitle', 'startYear']],
#        how='left',
#        left_on=['title', 'year'],
#        right_on=['primaryTitle', 'startYear']
#   )
#    return merged
    
def add_ratings(file_ratings,table):
    ratings = pd.read_csv(file_ratings,sep='\t', dtype = str)
    merged = table.merge(
    ratings[['tconst', 'averageRating', 'numVotes']],
    how='left',
    left_on=['tconst'],
    right_on=['tconst'])
    
    return merged

def add_genres(file_basics,table):
    genres = pd.read_csv(file_basics,sep='\t', dtype = str)
    merged = table.merge(
    genres[['tconst','genres']],
    how='left',
    left_on=['tconst'],
    right_on=['tconst'])
    
    return merged

def add_box_office(file_recette,table):
    box_office = pd.read_csv(file_recette, dtype = str)
    
    box_office['box_office'] = pd.to_numeric(
        box_office['box_office'],
        errors='coerce'
    )
    
    merged = table.merge(
    box_office[['title','box_office']],
    how='left',
    left_on=['title'],
    right_on=['title'])
    
    return merged

def movies_and_series_per_year(table_movie):

    df = table_movie.copy()
    df["startYear"] = df["startYear"].replace("\\N", pd.NA)
    df = df.dropna(subset=["startYear"])
    df["startYear"] = df["startYear"].astype(int)
    df = df[(df["startYear"] < 2026) & (df["startYear"] > 1980)]

    movies_per_year = (
        df[df["titleType"] == "movie"]
        .groupby("startYear")
        .size()
        .reset_index(name="nombre_de_films")
    )

    series_per_year = (
        df[df["titleType"] != "movie"]
        .groupby("startYear")
        .size()
        .reset_index(name="nombre_de_serie")
    )

    table_year = (
        pd.merge(movies_per_year, series_per_year, on="startYear", how="outer")
        .fillna(0)
        .sort_values("startYear")
    )

    table_year["nombre_de_films"] = table_year["nombre_de_films"].astype(int)
    table_year["nombre_de_serie"] = table_year["nombre_de_serie"].astype(int)

    return table_year
