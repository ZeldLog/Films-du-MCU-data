from Extract.extract import *
from Visualisation.movie_plot import *
from Visualisation.actor_plot import *
from Traitement.modification import *
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import sys

star_wars = ["tt22176242","tt0076759","tt0080684",
             "tt0086190","tt0120915","tt0121765",
             "tt0121766","tt0361243","tt0458290",
             "tt1185834","tt2488496","tt2527336",
             "tt2527338","tt2930604","tt3778644",
             "tt8111088","tt13668894","tt13622776"]

harry_potter = ["tt0241527","tt0295297","tt0304141",
                "tt0330373","tt0373889","tt0417741",
                "tt0926084","tt1201607","tt4123430",
                "tt4123432","tt3183660"]

dcu = ["tt0770828","tt2975590","tt0974015",
       "tt12361974","tt1477834","tt9663764",
       "tt0439572","tt0451279","tt7126948",
       "tt5950044","tt1877830"]

r_evil = ["tt0120804","tt0318627","tt0432021",
          "tt1174954","tt1220634","tt13173144",
          "tt1753496","tt1855325","tt2592614",
          "tt26240498","tt6920084"]

alien = ["tt0078748","tt0090605","tt0103644",
         "tt0118583","tt1446714","tt2316204",
         "tt18412256","tt0370263","tt0758730"]

def main():
    #film_file = 'data/film.csv'
    ratings_file = '../title.ratings.tsv'
    mcu_file = 'data/MCU_V3_5.csv'
    actor_file = 'data/Acteur.csv'
    name_file = 'data/name.csv'
 
    table_actor = pd.read_csv(actor_file)
    table_name = pd.read_csv(name_file)
    table_mcu = pd.read_csv(mcu_file)
    table_mcu['name'] = "MCU"
    
    # plot_acteur_rating(table_mcu,table_actor)
    # plot_personnage_apparitions(table_actor)
    plot_distribution_percentages(table_name,table_mcu)
    
    ### Comparaison notes par franchises ###
    # table_movie = pd.read_csv(film_file)
    # table_sw = filtrer_par_tconst(star_wars,table_movie,"Star Wars")
    # table_hp = filtrer_par_tconst(harry_potter,table_movie,"Harry Potter")
    # table_dcu = filtrer_par_tconst(dcu,table_movie,"DCU")
    # table_r_evil = filtrer_par_tconst(r_evil,table_movie,"Resident Evil")
    # table_alien = filtrer_par_tconst(alien,table_movie,"Alien")
    # dfs = [table_mcu,table_sw,table_hp,table_dcu,table_r_evil,table_alien]
    # plot_average_ratings_per_franchise(dfs)
    
    
    # table_movie.to_csv("./data/film.csv", index=False)
    # year_table = movies_and_series_per_year(table_movie)
    # plot_movies_and_series_per_year(year_table)
    
if __name__ == "__main__":
    main()