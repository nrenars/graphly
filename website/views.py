from flask import Blueprint, render_template, url_for, redirect, current_app, flash, jsonify, send_from_directory, request
from flask_login import current_user, login_user, login_required, logout_user
from .forms import GraphForm
from .graphs import pokemon_graph, tv_graph, generate_graph
from .models import User, Graph
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from werkzeug.utils import secure_filename
from . import db
from datetime import datetime

# app = create_app()
views = Blueprint('views', __name__)

matplotlib.use('Agg')

@views.route("/") 
def home(): 
	pokemon_graph()
	tv_graph()
	return render_template('home.html')

@views.route("/about") 
def about(): 
	return render_template('about.html')

@views.route("/make-graph", methods=['GET', 'POST'])
@login_required
def make_graph():
    form = GraphForm()
    
    if form.validate_on_submit():
        # Get the uploaded file
        file = form.data.data
        filename = secure_filename(file.filename)
        # Save the uploaded file
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate the graph
        graph_filename = f"graphs/{generate_graph(filepath).split('/')[-1]}"

        
        # Create a new graph entry for the user
        new_graph = Graph(
            data=filename,
            title=form.title.data,
            graph_image=graph_filename,
            user_id=current_user.id
        )
        db.session.add(new_graph)
        db.session.commit()
        flash("Check your account to see your graph")
        return render_template('make_graph.html', form=form, graph=graph_filename)

    # Fetch all graphs associated with the logged-in user
    user_graphs = Graph.query.filter_by(user_id=current_user.id).all()
    
    for graph in user_graphs:
        print(f"Graph Title: {graph.title}, Graph Image Path: {graph.graph_image}")
	
    return render_template('make_graph.html', form=form, user_graphs=user_graphs)

@views.route('/delete-graph', methods=['POST'])
def delete_graph():
    if request.json.get('action') == 'post':
        graph_filename = request.json.get('graph_filename')
        graph_path = os.path.join("website/static/", graph_filename)

        print(f"DEBUG: Trying to delete {graph_path}")  # Debugging print

        if os.path.exists(graph_path):
            os.remove(graph_path)
            flash("Graph deleted successfully!", "success")
            return jsonify({'message': "Graph deleted successfully."})
        else:
            print("DEBUG: File not found!")  # Debugging print
            flash("Graph not found!", "error")
            return jsonify({'error': "Graph not found."}), 404
