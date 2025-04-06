from flask import Flask, render_template, request, redirect, jsonify
from utils.db import db
from models.song import Song
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Song.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html', content=songs)


@app.route('/search', methods=['GET'])
def search_song():
    query = request.args.get('query', '')  # Get the search query from the request
    if query:
        # Query the database for matching songs
        results = Song.query.filter(
            (Song.song_name.ilike(f'%{query}%')) |
            (Song.artist.ilike(f'%{query}%'))
        ).all()
    else:
        results = []

    return render_template('search.html', content=results, query=query)


@app.route('/topsongs')
def topsongs():
    return render_template('topsongs.html')


@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    song_id = form_data.get('song_id')
    song_name = form_data.get('song_name')
    artist = form_data.get('artist')
    streamed_hours = form_data.get('streamed_hours')

    song = Song.query.filter_by(song_id=song_id).first()
    if not song:
        song = Song(
            song_id=song_id,
            song_name=song_name,
            artist=artist,
            streamed_hours=streamed_hours
        )
        db.session.add(song)
        db.session.commit()
    print("Submitted successfully")
    return redirect('/')


@app.route('/delete/<int:song_id>', methods=['GET', 'DELETE'])
def delete_song(song_id):
    song = Song.query.get(song_id)

    if not song:
        return jsonify({'message': 'Song not found'}), 404

    try:
        db.session.delete(song)
        db.session.commit()
        return jsonify({'message': 'Song deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {e}'}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
