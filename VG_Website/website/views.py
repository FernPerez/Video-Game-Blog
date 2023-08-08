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

        # Check validity of inputs and flash messages
        if len(title) < 1:
            flash("Title must be greater than 1 character.", category='error')
        elif len(platforms) < 1:
            flash("Platforms entry must be at least 1 character.", category='error')
        elif genre2 == genre1 or genre3 == genre1 or (genre2 == genre3 and genre2 != 'N/A'):
            flash("Cannot have two of the same genre.", category='error')
        elif releaseDate == '':
            flash('Must enter release date.', category='error')
        elif dateStarted == '':
            flash('Must enter date started.', category='error')
        elif len(description) > 5000:
            flash('Description cannot be longer than 5000 characters.', category='error')
        else:
            #Convert html dates to Python dates
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

            #add game to db
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

@views.route("/games", methods=["GET", "POST"])
def games():
    gameList = Game.query
    filteredList = []

    for game in gameList:
        filteredList.append(game)
    if request.method == 'POST':
        data = request.form
        print(data)

        sort_by = request.form.get("sorter")
        order = request.form.get("order")
        system = request.form.get("platform_select")

        listLength = len(filteredList)
        i = 0
        while i < listLength:
            if system == "NES" and "SNES" in filteredList[i].platforms:
                del filteredList[i]
                listLength -= 1
            elif system != "All" and system not in filteredList[i].platforms:
                del filteredList[i]
                listLength -= 1
            else:
                i += 1

        # if system == "All":
        #     return render_template("games.html", games=gameList, sort_by=sort_by, order=order) 
        # else:
        #     gameList = Game.query.filter_by(platforms=system)
        return render_template("games.html", games=filteredList, sort_by=sort_by, order=order) 
    return render_template("games.html", games=gameList, sort_by="default", order="default")

@views.route("/games/<title>")
def game(title):
    game = Game.query.filter_by(title=title).first_or_404()
    posts = [
        {'author': game, 'body': 'Test post #1'},
        {'author': game, 'body': 'Test post #2'}
    ]
    return render_template('game.html', game=game, posts=posts)