from flask import Blueprint, render_template, url_for, redirect, current_app, flash, jsonify, request
from flask_login import current_user, login_required
from .forms import GraphForm
from .graphs import pokemon_graph, tv_graph, generate_graph, gender_graph, pokemon_hist
from .models import Graph
import os
import matplotlib
from werkzeug.utils import secure_filename
from . import db

ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


views = Blueprint('views', __name__)

matplotlib.use('Agg')

@views.route("/") 
def home(): 
    pokemon_graph()
    tv_graph()
    gender_graph()
    pokemon_hist()

    return render_template('home.html')

@views.route("/about") 
def about(): 
	return render_template('about.html')

@views.route("/make-graph", methods=['GET', 'POST'])
@login_required
def make_graph():
    form = GraphForm()
    
    if form.validate_on_submit():
        file = form.file_upload.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        color = request.form.get('color')
        graph_type = request.form.get('graph_type')

        print(f"File path: {filepath}, Color: {color}, Graph Type: {graph_type}") 

        random_column, graph_url = generate_graph(filepath, color, graph_type)

        if graph_url is None:
            flash("Error: Graph generation failed. Please check your file format and try again.", "danger")
            return render_template('make_graph.html', form=form)

        graph_filename = f"graphs/{graph_url.split('/')[-1]}"

        print(f"Graph details: Title={random_column}, Graph Type={graph_type}, Image={graph_filename}")

        new_graph = Graph(
            data=filename,
            color=color,
            title=random_column,
            graph_type=graph_type,
            graph_image=graph_filename,
            user_id=current_user.id
        )

        db.session.add(new_graph)
        db.session.commit()

        flash("Graph has been generated successfully", "success")
        return redirect(url_for('auth.account', user_id=current_user.id))

    user_graphs = Graph.query.filter_by(user_id=current_user.id).all()

    return render_template('make_graph.html', form=form, user_graphs=user_graphs)

@views.route('/delete-graph', methods=['POST'])
def delete_graph():
    data = request.get_json()
    graph_filename = data.get('graph_filename')

    if not graph_filename:
        return jsonify({'error': 'No filename provided'}), 400

    graph = Graph.query.filter_by(graph_image=graph_filename, user_id=current_user.id).first()

    if not graph:
        return jsonify({'error': 'Graph not found'}), 404

    file_path = os.path.join(current_app.static_folder, graph.graph_image)

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(graph)
    db.session.commit()

    return jsonify({'message': 'Graph deleted successfully'}), 200

@views.route('/delete-all-graphs', methods=['POST'])
@login_required
def delete_all_graphs():
    try:
        graphs_to_delete = Graph.query.filter_by(user_id=current_user.id).all()
        
        for graph in graphs_to_delete:
            db.session.delete(graph)
        
        db.session.commit()

        return jsonify({'message': 'All graphs have been deleted successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500