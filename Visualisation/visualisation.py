import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd

def plot_film_rating_per_phases(table):
    phases_colors = {
        1: 'red',
        2: 'blue',
        3: 'green',
        4: 'purple',
        5: 'orange',
        6: 'brown'
    }
    
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
        loc="center left",          # point d’ancrage de la légende
        bbox_to_anchor=(1, 0.5)
    )
    
    

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
    
    
def plot_genre_ratings(table_global):
    
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