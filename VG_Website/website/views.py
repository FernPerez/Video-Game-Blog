from flask import Blueprint, render_template, request, flash, current_app
from .models import Game
from . import db
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=["GET"])
def home():
    return render_template("home.html")

@views.route('/about', methods=["GET"])
def about():
    return render_template("about.html")

@views.route('/add-game', methods=["GET", "POST"])
def addGame():
    data = request.form
    if request.method == 'POST':
        title = request.form.get('title')
        platforms = request.form.get('platforms')
        series = request.form.get('series')
        franchise = request.form.get('franchise')
        genre1 = request.form.get('genre1')
        genre2 = request.form.get('genre2')
        genre3 = request.form.get('genre3')
        releaseDate = request.form.get('releaseDate')
        dateStarted = request.form.get('dateStarted')
        dateFinished = request.form.get('dateFinished')
        description = request.form.get('description')
        score = request.form.get('score')
        gameCover = request.files.get('gameCover')

        releaseDate = datetime.strptime(releaseDate, '%Y-%m-%d')
        releaseDate = releaseDate.date()
        dateStarted = datetime.strptime(dateStarted, '%Y-%m-%d')
        dateStarted = dateStarted.date()
        dateFinished = datetime.strptime(dateFinished, '%Y-%m-%d')
        dateFinished = dateFinished.date()

        # Convert blanks to None (NULL in db)
        if series == '':
            series = None
        if franchise == '':
            franchise == None
        if genre2 == 'N/A':
            genre2 = None
        if genre3 == 'N/A':
            genre3 = None
        if gameCover == '':
            gameCover = None
        else:
            gameCoverName = secure_filename(gameCover.filename)
            gameCoverName = str(uuid.uuid1()) + "_" + gameCoverName

        # Check validity of inputs and flash messages
        if len(title) < 1:
            flash("Title must be greater than 1 character.", category='error')
        elif len(platforms) < 1:
            flash("Platforms entry must be at least 1 character.", category='error')
        elif genre2 == genre1 or genre3 == genre1 or (genre2 == genre3 and genre2 != None):
            flash("Cannot have two of the same genre.", category='error')
        elif releaseDate == '':
            flash('Must enter release date.', category='error')
        elif dateStarted == '':
            flash('Must enter date started.', category='error')
        elif len(description) > 5000:
            flash('Description cannot be longer than 5000 characters.', category='error')
        else:
            #add game to db
            print(data)
            print(gameCover)
            print(os.getcwd())
            new_game = Game(
                title = title,
                platforms = platforms,
                series = series,
                franchise = franchise,
                genre1 = genre1,
                genre2 = genre2,
                genre3 = genre3,
                releaseDate = releaseDate,
                dateStarted = dateStarted,
                dateFinished = dateFinished,
                description = description,
                score = score,
                gameCover = gameCoverName
            )
            gameCover.save(os.path.join(current_app.config["UPLOAD_FOLDER"], gameCoverName))
            db.session.add(new_game)
            db.session.commit()
            flash('Game added!', category='success')



    return render_template("addGame.html")

@views.route("/games", methods=["GET"])
def games():
    return render_template("games.html")