import pandas as pd
import matplotlib.pyplot as plt
import os
from flask import current_app, url_for
from datetime import datetime
import random


def pokemon_graph():
    pokemon_df = pd.read_csv("website/static/data/Pokemon.csv")
    type1 = pokemon_df['Type 1'].value_counts().reset_index()
    type1.columns = ['Type', 'Count']
    type1.plot(x='Type', y='Count', kind='bar', color='snow', edgecolor='red')
    plt.title('Most common pokemon types')
    plt.xlabel('Type 1')
    plt.ylabel('Count')
    plt.savefig("website/static/images/pokemon_graph.png")

def tv_graph():
    tv_df = pd.read_csv("website/static/data/tvmarketing.csv")
    plt.figure(figsize=(8, 5))
    plt.scatter(tv_df['TV'], tv_df['Sales'], color='blue', alpha=0.6)
    plt.title('TV Marketing vs Sales', fontsize=14)
    plt.xlabel('TV Advertising Budget', fontsize=12)
    plt.ylabel('Sales Revenue', fontsize=12)
    plt.grid(True)

    plt.savefig("website/static/images/tv_graph.png")


def generate_graph(filepath):
    df = pd.read_csv(filepath)

    # Ensure the graphs folder exists
    graph_folder = current_app.config['GRAPHS_FOLDER']
    if not os.path.exists(graph_folder):
        os.makedirs(graph_folder)

    # Choose a random column that has data
    valid_columns = [col for col in df.columns if not df[col].dropna().empty]
    
    if not valid_columns:
        return None  # No valid data to plot
    
    random_column = random.choice(valid_columns)  # Pick one column

    # Get value counts
    value_counts = df[random_column].value_counts()

    # Limit the number of bins for readability (max 20 bins, for example)
    max_bins = 20
    if len(value_counts) > max_bins:
        # If the number of unique values is more than max_bins, take the most frequent ones
        value_counts = value_counts.head(max_bins)

    # Create the plot
    plt.figure(figsize=(12, 10))
    value_counts.plot(kind='bar', color='red')

    plt.xlabel(random_column)
    plt.ylabel("Count")
    plt.title(f"{random_column} Count")
    plt.grid(axis='y')

    # Define a unique filename
    graph_filename = f"{random_column}_{datetime.utcnow().timestamp()}.png"
    graph_path = os.path.join(graph_folder, graph_filename)

    # Save the figure
    plt.savefig(graph_path)
    plt.close()

    # Return the graph URL
    return url_for('static', filename=f'graphs/{graph_filename}')