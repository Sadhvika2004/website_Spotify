from utils.db import db


class Song(db.Model):
    __tablename__ = 'song'

    song_id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    streamed_hours = db.Column(db.Integer, nullable=False)
