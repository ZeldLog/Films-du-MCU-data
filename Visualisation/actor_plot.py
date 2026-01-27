import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import matplotlib.ticker as ticker
from Traitement.modification import *

def plot_acteur_rating(table_global,table_actor):
    
    table_actor['Productions'] = table_actor['Productions'].apply(lambda x: x.split('; '))
    table_actor = table_actor.explode('Productions').rename(columns={'Productions': 'title'})
    
    df_merged = pd.merge(table_actor, table_global, on='title', how='left')
    df_merged = df_merged.dropna()

    df_moyenne = df_merged.groupby('Character')['box_office'].mean().reset_index().sort_values('box_office', ascending=False)
    
    fig, ax = plt.subplots(figsize=(16,9))
    df_moyenne.plot(kind='bar', x='Character', y='box_office', legend=False, ax=ax, rot=45)

    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f"{int(x):,} $")
    )
    ax.set_xticklabels(df_moyenne['Character'], rotation=45, ha='right') 
    ax.tick_params(axis='x', pad=8)

    plt.title("Moyenne des notes des films du MCU dans lequelle il a jouer", fontsize=14)
    plt.xlabel("Personnage",fontsize=14)
    plt.ylabel("Moyenne des notes des films du MCU",fontsize=14)
    plt.ylim(0, 2_000_000_000)
    plt.tight_layout()
    plt.bar(df_moyenne['Character'], df_moyenne['box_office'])
    plt.show()
    
def plot_personnage_apparitions(table_actor):

    table_actor = table_actor.copy()

    # Séparer les films et exploser
    table_actor['Productions'] = table_actor['Productions'].apply(lambda x: x.split('; '))
    table_actor = table_actor.explode('Productions')

    # Compter le nombre d'apparitions par personnage
    df_apparitions = (
        table_actor
        .groupby('Character')
        .size()
        .reset_index(name='MCU_Appearances')
        .sort_values('MCU_Appearances', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(16, 9))

    ax.bar(
        df_apparitions['Character'],
        df_apparitions['MCU_Appearances'],
        color='darkorange'
    )

    ax.set_title(
        "Nombre d'apparitions des personnages dans le MCU",
        fontsize=16
    )
    ax.set_xlabel("Personnage", fontsize=14)
    ax.set_ylabel("Nombre d'apparitions", fontsize=14)

    # Gestion des labels longs
    ax.set_xticklabels(df_apparitions['Character'], rotation=45, ha='right')
    fig.subplots_adjust(bottom=0.35)

    plt.show()
    
def plot_distribution_percentages(df_actors,df_movies):
    
    df_actors = add_percentage_movies(df_actors, df_movies)
    # Forcer l’ordre et les valeurs attendues
    order = [0, 25, 50, 75, 100]

    counts = (
        df_actors["pourcentage_films"]
        .round(0)
        .astype(int)
        .value_counts()
        .reindex(order, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(order, counts.values, width=15, color="steelblue")

    ax.set_title(
        "Répartition des acteurs selon le pourcentage de popularité obtenue avec un films du MCU ",
        fontsize=14
    )
    ax.set_xlabel("Pourcentage selon le nombre de films du MCU présent dans la liste ayant rendu célèbre l'acteur", fontsize=12)
    ax.set_ylabel("Nombre de personnes", fontsize=12)

    ax.set_xticks(order)
    ax.set_xticklabels([f"{x}%" for x in order])

    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.show()