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