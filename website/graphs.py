import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from flask import current_app, url_for
from datetime import datetime
import random

def pokemon_graph():
    pokemon_df = pd.read_csv("website/static/data/Pokemon.csv")
    type1 = pokemon_df['Type 1'].value_counts().reset_index()
    type1.columns = ['Type', 'Count']
    type1.plot(x='Type', y='Count', kind='bar', color='red')
    plt.title('Most common pokemon types')
    plt.xlabel('Type 1')
    plt.ylabel('Count')
    plt.savefig("website/static/images/pokemon_graph.png")

def tv_graph():
    tv_df = pd.read_csv("website/static/data/tvmarketing.csv")
    plt.figure(figsize=(8, 5))
    plt.scatter(tv_df['TV'], tv_df['Sales'], color='blue')
    plt.title('TV Marketing vs Sales', fontsize=14)
    plt.xlabel('TV Advertising Budget', fontsize=12)
    plt.ylabel('Sales Revenue', fontsize=12)
    plt.grid(True)

    plt.savefig("website/static/images/tv_graph.png")

def gender_graph():
    genders_df = pd.read_csv("website/static/data/IHME_GBD_2010_MORTALITY_AGE_SPECIFIC_BY_COUNTRY_1970_2010.csv")
    country = genders_df[genders_df['Country Name'] == 'Latvia']
    gender = country['Sex'].value_counts().reset_index() 
    gender.columns = ['Sex', 'Count']
    gender.plot(x='Sex', y='Count', kind='barh', color='blue')
    plt.title('Gender Distribution in Latvia')
    plt.xlabel('Count')
    plt.ylabel('Gender')
    plt.savefig("website/static/images/IHME_GBD_2010_MORTALITY_AGE_SPECIFIC_BY_COUNTRY_1970_2010.png")
    plt.close()  

def pokemon_hist():
    pokemon_df = pd.read_csv("website/static/data/Pokemon.csv")
    pokemon_df.hist(column='Defense', bins=10, orientation='horizontal')
    plt.savefig("website/static/images/pokemon_hist.png")

def generate_graph(filepath, color, graph_type):
    try:
        df = pd.read_csv(filepath, delimiter=",", on_bad_lines="skip")
        graph_folder = current_app.config['GRAPHS_FOLDER']
        os.makedirs(graph_folder, exist_ok=True)

        valid_columns = [col for col in df.columns if not df[col].dropna().empty]
        if not valid_columns:
            print("No valid data found in CSV.")  
            return None, None 

        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        random_column = random.choice(numeric_columns if numeric_columns else valid_columns)
        print(f"Selected column: {random_column}")

        available_graph_types = ['bar','barh','histogram', 'scatter', 'heatmap']
        if graph_type == 'random':
            graph_type = random.choice(available_graph_types)
            print(f"Randomly selected graph type: {graph_type}")

        if color == 'random':
            color = random.choice([
                'red', 'green', 'blue', 'yellow', 'orange', 'pink', 
                'purple', 'brown', 'gray', 'black', 'cyan', 'magenta', 
                'lime', 'indigo', 'violet', 'teal', 'navy', 'maroon'
            ])

        plt.figure(figsize=(12, 8))

        if graph_type == 'bar':
            value_counts = df[random_column].value_counts()
            value_counts.plot(kind='bar', color=color)
            plt.xlabel(random_column)
            plt.ylabel("Count")
            plt.title(f"{random_column} Count")

        elif graph_type == 'barh':
            value_counts = df[random_column].value_counts()
            value_counts.plot(kind='barh', color=color)
            plt.xlabel(random_column)
            plt.ylabel("Count")
            plt.title(f"{random_column} Count")

        elif graph_type == 'histogram':
            df[random_column].hist(bins=15, color=color, edgecolor='black')
            plt.xlabel(random_column)
            plt.ylabel("Frequency")
            plt.title(f"Histogram of {random_column}")

        elif graph_type == 'scatter':
            if len(numeric_columns) < 2:
                return None, None  
            x_column, y_column = random.sample(numeric_columns, 2)
            plt.scatter(df[x_column], df[y_column], color=color, alpha=0.6)
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f"Scatter Plot: {x_column} vs {y_column}")

        elif graph_type == 'heatmap':
            if len(numeric_columns) < 2:
                return None, None  
            corr_matrix = df[numeric_columns].corr()
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
            plt.title("Heatmap of Correlations")

        else:
            print("Invalid graph type selected")
            return None, None

        graph_filename = f"{graph_type}_{random_column}_{datetime.utcnow().timestamp():.6f}.png"
        graph_filename = graph_filename.replace(' ', '_') 
        graph_path = os.path.join(graph_folder, graph_filename)

        print(f"Saving graph to: {graph_path}") 
        plt.savefig(graph_path)
        plt.close()

        return random_column, url_for('static', filename=f'graphs/{graph_filename}')

    except pd.errors.ParserError as e:
        print("CSV Parsing Error:", e)
        return None, None  

    except Exception as e:
        print("Unexpected Error:", e)
        return None, None  