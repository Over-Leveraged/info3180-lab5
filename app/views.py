"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename
from .forms import MovieForm
from .models import db, Movies
from flask_wtf.csrf import generate_csrf




###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    
    if request.method == 'GET': 
        movies = db.session.execute(db.select(Movies)).scalars()
        results = [
            {
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'poster': movie.poster
            } for movie in movies]
        return jsonify(movies = results)
    
    form = MovieForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster = form.poster.data
        
        filename = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            movie = Movies(title, description, filename)
            db.session.add(movie)
            db.session.commit()

        except Exception as e:
            return jsonify(message="Movie could not be added", error=str(e))


        Added_response = {
            'message': 'Movie Successfully added',
            'title': movie.title,
            'poster': movie.poster,
            'description': movie.description
        }
        return jsonify(Added_response), 201

    else:
        return jsonify(message="Movie could not be added", errors=form_errors(form))
    
@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    #movies = Movies.query.all()
    movies = db.session.execute(db.select(Movies)).scalars()
    results = [
        {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': movie.poster
        } for movie in movies]
    return jsonify(movies = results)

@app.route("/api/v1/posters/<filename>")
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)
    

    
#@app.route('api/v1/movies', methods=['GET'])
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})
        


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404