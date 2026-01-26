import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import matplotlib.ticker as ticker

def plot_film_rating_per_phases(table):
    phases_colors = {
        1: 'red',
        2: 'blue',
        3: 'green',
        4: 'purple',
        5: 'orange',
        6: 'brown'
    }
    
    table = table[table['film/tv'] == "Film"].copy()
    
    phases = table['phase'].tolist()
    colors = [phases_colors[int(p)] for p in phases]
    
    
    fig, ax = plt.subplots(figsize=(16,9))
    table.plot(kind='bar', x='title', y='averageRating', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(table['title'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Notation des films du MCU SUR IMDB", fontsize=14)
    plt.xlabel("Films",fontsize=14)
    plt.ylabel("Note",fontsize=14)
    plt.ylim(0, 10)
    plt.bar(table['title'], table['averageRating'], color=colors)
    
    legend_elements = [
        Patch(facecolor=color, label=f"Phase {phase}")
        for phase, color in phases_colors.items()
    ]

    ax.legend(
        handles=legend_elements,
        title="Phases du table",
        loc="center left",  
        bbox_to_anchor=(1, 0.5)
    )
    
    

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
    

def plot_series_rating_per_phases(table):
    phases_colors = {
        1: 'red',
        2: 'blue',
        3: 'green',
        4: 'purple',
        5: 'orange',
        6: 'brown'
    }
    
    table = table[table['film/tv'] == "TV (Disney+)"].copy()
    
    phases = table['phase'].tolist()
    colors = [phases_colors[int(p)] for p in phases]
    
    
    fig, ax = plt.subplots(figsize=(16,9))
    table.plot(kind='bar', x='title', y='averageRating', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(table['title'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Notation des Séries du MCU SUR IMDB", fontsize=14)
    plt.xlabel("Séries",fontsize=14)
    plt.ylabel("Note",fontsize=14)
    plt.ylim(0, 10)
    plt.bar(table['title'], table['averageRating'], color=colors)
    
    legend_elements = [
        Patch(facecolor=color, label=f"Phase {phase}")
        for phase, color in phases_colors.items()
    ]

    ax.legend(
        handles=legend_elements,
        title="Phases du table",
        loc="center left",  
        bbox_to_anchor=(1, 0.5)
    )
    
    

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
    
    
def plot_genre_ratings(table_global):
    
    table_global["genres"] = table_global["genres"].str.split(",")

    table= table_global.explode("genres")

    table = (
        table
        .groupby("genres")
        .agg(
            count=("title", "count"),
            average_rating=("averageRating", "mean")
        )
        .reset_index()
    )
    print(table)
    
    fig, ax = plt.subplots(figsize=(16,9))
    table.plot(kind='bar', x='genres', y='average_rating', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(table['genres'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Moyenne des notes par genre du MCU SUR IMDB", fontsize=14)
    plt.xlabel("Genres",fontsize=14)
    plt.ylabel("Note",fontsize=14)
    plt.ylim(0, 10)
    plt.bar(table['genres'], table['average_rating'])
    
    plt.show()
    
def plot_film_box_office_per_phases(table):
    phases_colors = {
        1: 'red',
        2: 'blue',
        3: 'green',
        4: 'purple',
        5: 'orange',
        6: 'brown'
    }
    films = table[table['film/tv'] == "Film"]
    phases = films['phase'].tolist()
    colors = [phases_colors[int(p)] for p in phases]
    
    
    fig, ax = plt.subplots(figsize=(16,9))
    films.plot(kind='bar', x='title', y='box_office', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(films['title'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Box office mondiale des films du MCU", fontsize=14)
    plt.xlabel("Films",fontsize=14)
    plt.ylabel("Box Office(en dollars américain)",fontsize=14)
    plt.ylim(0, 3_000_000_000)
    plt.bar(films['title'], films['box_office'], color=colors)
    
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f"{int(x):,} $")
    )
    
    legend_elements = [
        Patch(facecolor=color, label=f"Phase {phase}")
        for phase, color in phases_colors.items()
    ]

    ax.legend(
        handles=legend_elements,
        title="Phases du table",
        loc="center left",    
        bbox_to_anchor=(1, 0.5)
    )
    
    

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
    

def plot_film_box_office_yearly_average(table):
    phases_colors = {
        1: 'red',
        2: 'blue',
        3: 'green',
        4: 'purple',
        5: 'orange',
        6: 'brown'
    }

    films = table[table['film/tv'] == "Film"].copy()

    films['release date'] = pd.to_datetime(films['release date'], format='%Y-%m')
    films['year'] = films['release date'].dt.year

    yearly_avg = (
        films
        .groupby('year')
        .agg(
            box_office_mean=('box_office', 'mean'),
            dominant_phase=('phase', lambda x: x.mode()[0])
        )
        .reset_index()
        .sort_values('year')
    )

    fig, ax = plt.subplots(figsize=(16, 9))


    start_year = yearly_avg['year'][0]
    current_phase = yearly_avg['dominant_phase'][0]

    for i in range(1, len(yearly_avg)):
        if yearly_avg['dominant_phase'][i] != current_phase:
            ax.axvspan(
                start_year - 0.5,
                yearly_avg['year'][i] - 0.5,
                color=phases_colors[int(current_phase)],
                alpha=0.15
            )
            start_year = yearly_avg['year'][i]
            current_phase = yearly_avg['dominant_phase'][i]
    ax.axvspan(
        start_year - 0.5,
        yearly_avg['year'].iloc[-1] + 0.5,
        color=phases_colors[int(current_phase)],
        alpha=0.15
    )

    ax.plot(
        yearly_avg['year'],
        yearly_avg['box_office_mean'],
        color='black',
        linewidth=2,
        marker='o'
    )

    plt.title("Box-office moyen annuel des films du MCU", fontsize=14)
    plt.xlabel("Année de sortie", fontsize=14)
    plt.ylabel("Box Office moyen (en dollars américains)", fontsize=14)
    plt.ylim(0, 2_000_000_000)
    
    ax.set_xlim(yearly_avg['year'].min() - 0.5, yearly_avg['year'].max() + 0.5)

    ax.set_xticks(range(yearly_avg['year'].min(), yearly_avg['year'].max() + 1))
    ax.set_xticklabels(range(yearly_avg['year'].min(), yearly_avg['year'].max() + 1), rotation=45)

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f"{int(x):,} $")
    )

    legend_elements = [
        Patch(facecolor=color, label=f"Phase {phase}")
        for phase, color in phases_colors.items()
    ]

    ax.legend(
        handles=legend_elements,
        title="Phase dominante de l’année",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
    
    
def plot_genre_ratings(table_global):
    
    table_global["genres"] = table_global["genres"].str.split(",")

    table= table_global.explode("genres")

    # Agrégation : nombre d'apparitions et moyenne de la note
    table = (
        table
        .groupby("genres")
        .agg(
            count=("title", "count"),
            average_rating=("averageRating", "mean")
        )
        .reset_index()
    )
    print(table)
    
    fig, ax = plt.subplots(figsize=(16,9))
    table.plot(kind='bar', x='genres', y='average_rating', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(table['genres'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Moyenne des notes par genre du MCU SUR IMDB", fontsize=14)
    plt.xlabel("Genres",fontsize=14)
    plt.ylabel("Note",fontsize=14)
    plt.ylim(0, 10)
    plt.bar(table['genres'], table['average_rating'])
    
    plt.show()
    
def plot_genre_count(table_global):
    
    table_global["genres"] = table_global["genres"].str.split(",")

    # On "explose" la liste pour avoir 1 genre par ligne
    table= table_global.explode("genres")

    # Agrégation : nombre d'apparitions et moyenne de la note
    table = (
        table
        .groupby("genres")
        .agg(
            count=("title", "count"),
            average_rating=("averageRating", "mean")
        )
        .reset_index()
    )
    print(table)
    
    fig, ax = plt.subplots(figsize=(16,9))
    table.plot(kind='bar', x='genres', y='count', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(table['genres'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Nombre de Film par genre du MCU SUR IMDB", fontsize=14)
    plt.xlabel("Genres",fontsize=14)
    plt.ylabel("Note",fontsize=14)
    plt.ylim(0, 60)
    plt.bar(table['genres'], table['count'])
    
    plt.show()
    
    
def plot_acteur_rating(table_global,table_actor):
    
    table_actor['Productions'] = table_actor['Productions'].apply(lambda x: x.split('; '))
    table_actor = table_actor.explode('Productions').rename(columns={'Productions': 'title'})
    
    df_merged = pd.merge(table_actor, table_global, on='title', how='left')
    df_merged = df_merged.dropna()

    df_moyenne = df_merged.groupby('Actor')['box_office'].mean().reset_index().sort_values('box_office', ascending=False)
    
    fig, ax = plt.subplots(figsize=(16,9))
    df_moyenne.plot(kind='bar', x='Actor', y='box_office', legend=False, ax=ax, rot=45)

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f"{int(x):,} $")
    )
    ax.set_xticklabels(df_moyenne['Actor'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Moyenne des box_office par acteurs du MCU SUR IMDB", fontsize=14)
    plt.xlabel("Actor",fontsize=14)
    plt.ylabel("box_office",fontsize=14)
    plt.ylim(0, 2_000_000_000)
    plt.bar(df_moyenne['Actor'], df_moyenne['box_office'])
    plt.show()
    
    
def plot_movie_per_year(table_year):
    fig, ax = plt.subplots(figsize=(16,9))
    table_year.plot(kind='bar', x='startYear', y='nombre_de_films', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(table_year['startYear'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Nombre de Film par année", fontsize=14)
    plt.xlabel("Année",fontsize=14)
    plt.ylabel("Nombre de Film",fontsize=14)
    plt.bar(table_year['startYear'], table_year['nombre_de_films'])
    
    plt.show()
    
    
def plot_serie_per_year(table_year):
    fig, ax = plt.subplots(figsize=(16,9))
    table_year.plot(kind='bar', x='startYear', y='nombre_de_serie', legend=False, ax=ax, rot=45)

    ax.set_xticklabels(table_year['startYear'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Nombre de série par année", fontsize=14)
    plt.xlabel("Année",fontsize=14)
    plt.ylabel("Nombre de série",fontsize=14)
    plt.bar(table_year['startYear'], table_year['nombre_de_serie'])
    
    plt.show()


def plot_movies_and_series_per_year(table_year):
    fig, ax = plt.subplots(figsize=(16, 9))
    
    ax.set_xlim(
    table_year['startYear'].min() + 1,
    table_year['startYear'].max() + 1
    )
    
    ax.axvspan(
        2019,
        table_year['startYear'].max() + 1,
        color='red',
        alpha=0.15,
    )

    ax.plot(
        table_year['startYear'],
        table_year['nombre_de_films'],
        marker='o',
        label='Films'
    )

    ax.plot(
        table_year['startYear'],
        table_year['nombre_de_serie'],
        marker='o',
        label='Séries'
    )

    ax.set_title("Nombre de films et de séries par année", fontsize=14)
    ax.set_xlabel("Année", fontsize=14)
    ax.set_ylabel("Nombre", fontsize=14)
    ax.set_xticks(table_year['startYear'])
    ax.set_xticklabels(table_year['startYear'], rotation=45, ha='right')
    ax.tick_params(axis='x', pad=8)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.show()
    
    

def plot_average_ratings_per_franchise(dfs):

    if not dfs:
        print("La liste de DataFrames est vide.")
        return
    
    moyennes = []
    labels = []
    
    for i, df in enumerate(dfs):
        if 'averageRating' not in df.columns:
            raise ValueError(f"Le DataFrame {i} ne contient pas la colonne 'averageRating'")
        if 'name' not in df.columns:
            raise ValueError(f"Le DataFrame {i} ne contient pas la colonne 'name'")
        
        moyennes.append(df['averageRating'].mean())
        labels.append(df['name'].iloc[0])  # on prend le premier nom de la colonne name
    
    # Affichage du plot
    plt.figure(figsize=(8,5))
    plt.bar(labels, moyennes, color='skyblue')
    plt.ylim(0,10)
    plt.xlabel("Franchise")
    plt.ylabel("Moyenne des avis")
    plt.title("Moyenne de avis sur les films populaire des franchises")
    plt.show()
    
    return moyennes 