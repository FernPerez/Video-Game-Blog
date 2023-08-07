from . import db
from flask_login import UserMixin

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    platforms = db.Column(db.String(300), nullable=False)
    series = db.Column(db.String(200), nullable=True)
    franchise = db.Column(db.String(200), nullable=True)
    genre1 = db.Column(db.String(50), nullable=False)
    genre2 = db.Column(db.String(50), nullable=True)
    genre3 = db.Column(db.String(50), nullable=True)
    releaseDate = db.Column(db.Date, nullable=False)
    dateStarted = db.Column(db.Date, nullable=False)
    dateFinished = db.Column(db.Date, nullable=True)
    description = db.Column(db.String(5000), nullable=True)
    score = db.Column(db.Float, nullable=False)
    gameCover = db.Column(db.String(), unique=True, nullable=True)
