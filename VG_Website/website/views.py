from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for
from .models import Game
from . import db
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from datetime import datetime
import json
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=["GET"])
def home():
    return render_template("home.html", user=current_user)

@views.route('/about', methods=["GET"])
def about():
    return render_template("about.html", user=current_user)



@views.route('/add-game', methods=["GET", "POST"])
@login_required
def addGame():
    try:
        print(current_user.id)
    except:
        print("Error")
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
        gameCover = request.form.get('gameCover')

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
            try:
                dateFinished = datetime.strptime(dateFinished, '%Y-%m-%d')
                dateFinished = dateFinished.date()
            except:
                dateFinished = None

            # Convert blanks to None (NULL in db)
            if series == '':
                series = None
            if franchise == '':
                franchise == None
            if genre2 == 'N/A':
                genre2 = ''
            if genre3 == 'N/A':
                genre3 = ''
            # if gameCover.filename == '':
            #     gameCover = None
            #     gameCoverName = None
            # else:
            #     gameCoverName = secure_filename(gameCover.filename)
            #     gameCoverName = str(uuid.uuid1()) + "_" + gameCoverName

            #add game to db
            if gameCover != "N/A":
                gameCover = gameCover + ".jpg"
            else:
                gameCover = "placeholder.png"

            new_game = Game(
                title = title,
                user_id = current_user.id,
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
                gameCover = gameCover
            )
            try:
                db.session.add(new_game)
                db.session.commit()
                flash('Game added!', category='success')
            except:
                flash("Something went wrong...", category="error")



    return render_template("addGame.html", user=current_user)

@views.route("/games", methods=["GET", "POST"])
@login_required
def games():
    gameList = Game.query.filter_by(user_id=current_user.id)
    filteredList = []

    for game in gameList:
        filteredList.append(game)

    if request.method == 'POST':
        # data = request.form
        # print(data)

        search = request.form.get("searchbar")
        sort_by = request.form.get("sorter")
        order = request.form.get("order")
        system = request.form.get("platform_select")
        franchise = request.form.get("franchise_select")
        series = request.form.get("series_select")
        genre = request.form.get("genre_select")

        listLength = len(filteredList)
        i = 0
        while i < listLength:
            if search != "" and search not in filteredList[i].title:
                del filteredList[i]
                listLength -= 1                
            elif system == "NES" and "SNES" in filteredList[i].platforms:
                del filteredList[i]
                listLength -= 1
            elif system != "All" and system not in filteredList[i].platforms:
                del filteredList[i]
                listLength -= 1
            elif franchise != 'All' and franchise != filteredList[i].franchise:
                del filteredList[i]
                listLength -= 1
            elif series != 'All' and series != filteredList[i].series:
                del filteredList[i]
                listLength -= 1  
            elif genre != 'All' and genre != filteredList[i].genre1 and genre != filteredList[i].genre2 and genre != filteredList[i].genre3:   
                del filteredList[i]
                listLength -= 1 
            else:
                i += 1
        print(len(filteredList))
        count = len(filteredList)

        return render_template("games.html", games=filteredList, sort_by=sort_by, order=order, count=count, user=current_user) 
    
    print(len(filteredList))
    count = len(filteredList)
    return render_template("games.html", games=gameList, sort_by="default", order="default", count=count, user=current_user)

@views.route("/<username>/games/<id>", methods = ["GET", "POST"])
@login_required
def game(username, id):
    game = Game.query.filter_by(id=id).first_or_404()
    if game.user_id != current_user.id:
        flash("That game entry is not tied to this account. You are not allowed to view it.", category="error")
        return redirect(url_for('views.home'))
    if request.method == "POST":
        return redirect(url_for('views.updateGame', id=game.id, user=current_user, username=username))

    return render_template('game.html', game=game, user=current_user)

@views.route("/<username>/games/<id>/update", methods = ["GET", "POST"])
@login_required
def updateGame(username, id):
    gameToUpdate = Game.query.filter_by(id=id).first_or_404()
    if gameToUpdate.user_id != current_user.id:
        flash("That game entry is not tied to this account. You are not allowed to modify it.", category="error")
        return redirect(url_for('views.home'))
    if request.method == "POST":
        newTitle = request.form.get("title")
        newPlatforms = request.form.get("platforms")
        newSeries = request.form.get("series")
        newFranchise = request.form.get("franchise")
        newGenre1 = request.form.get("genre1")
        newGenre2 = request.form.get("genre2")
        newGenre3 = request.form.get("genre3")
        newRelease = request.form.get('releaseDate')
        newDS = request.form.get('dateStarted')
        newDF = request.form.get('dateFinished')
        newDesc = request.form.get('description')
        newScore = request.form.get('score')
        newGameCover = request.form.get('gameCover')

        # Check validity of inputs and flash messages
        if len(newTitle) < 1:
            flash("Title must be greater than 1 character.", category='error')
        elif len(newPlatforms) < 1:
            flash("Platforms entry must be at least 1 character.", category='error')
        elif newGenre2 == newGenre1 or newGenre3 == newGenre1 or (newGenre2 == newGenre3 and newGenre2 != 'N/A'):
            flash("Cannot have two of the same genre.", category='error')
        elif newRelease == '':
            flash('Must enter release date.', category='error')
        elif newDS == '':
            flash('Must enter date started.', category='error')
        elif len(newDesc) > 5000:
            flash('Description cannot be longer than 5000 characters.', category='error')
        else:

            # Convert html dates to Python dates
            newRelease = datetime.strptime(newRelease, '%Y-%m-%d')
            newRelease = newRelease.date()
            newDS = datetime.strptime(newDS, '%Y-%m-%d')
            newDS = newDS.date()
            try:
                newDF = datetime.strptime(newDF, '%Y-%m-%d')
                newDF = newDF.date()
            except:
                newDF = None

            # Convert blanks to None (NULL in db)
            if newSeries == '':
                newSeries = None
            if newFranchise == '':
                newFranchise == None
            if newGenre2 == 'N/A':
                newGenre2 = ''
            if newGenre3 == 'N/A':
                newGenre3 = ''
            if newGameCover != 'N/A':
                newGameCover = newGameCover + ".jpg"
            else:
                newGameCover = "placeholder.png"


            # Update values
            gameToUpdate.title = newTitle
            gameToUpdate.platforms = newPlatforms
            gameToUpdate.series = newSeries
            gameToUpdate.franchise = newFranchise
            gameToUpdate.genre1 = newGenre1
            gameToUpdate.genre2 = newGenre2
            gameToUpdate.genre3 = newGenre3
            gameToUpdate.releaseDate = newRelease
            gameToUpdate.dateStarted = newDS
            gameToUpdate.dateFinished = newDF
            gameToUpdate.description = newDesc
            gameToUpdate.score = newScore
            gameToUpdate.gameCover = newGameCover

            # Check if game cover or music has been updated, skip if not
            # if request.files.get('gameCover') and request.files.get('gameCover').filename != gameToUpdate.gameCover:
            #     newGameCoverName = request.files.get('gameCover').filename
            #     newGameCoverName = secure_filename(newGameCoverName)
            #     newGameCoverName = str(uuid.uuid1()) + "_" + newGameCoverName
            #     gameToUpdate.gameCover = newGameCoverName

            # print(request.files.get('gameMusic').filename)
            # if request.files.get('gameMusic') and request.files.get('gameMusic').filename != gameToUpdate.gameMusic:
            #     print("test2")
            #     newGameMusicName = request.files.get('gameMusic').filename
            #     newGameMusicName = secure_filename(newGameMusicName)
            #     newGameMusicName = str(uuid.uuid1()) + "_" + newGameMusicName
            #     gameToUpdate.gameMusic = newGameMusicName        

            # Save new files
            try:
                # if newGameCoverName != '':
                #     request.files.get('gameCover').save(os.path.join(current_app.config["UPLOAD_FOLDER"], f'images/{newGameCoverName}'))
                # if newGameMusicName != '':
                #     request.files.get('gameMusic').save(os.path.join(current_app.config["UPLOAD_FOLDER"], f'music/{newGameMusicName}'))

                db.session.commit()
                flash("Success!", category="success")
                return redirect(url_for('views.game', id=gameToUpdate.id, user=current_user, username=username))
            except:
                flash("Error", category="error")

    genres = [gameToUpdate.genre1, gameToUpdate.genre2, gameToUpdate.genre3]
    cover = gameToUpdate.gameCover[0:-4]
    return render_template('update_game.html', game=gameToUpdate, genres=json.dumps(genres), cover=cover, user=current_user, username=username)

# Functions below allow renaming an entry in the db if it has no title.

# @views.route("/games/X2", methods = ["GET", "POST"])
# def X2():
#     game = Game.query.filter_by(id=2).first_or_404()
#     if request.method == "POST":
#         return redirect(url_for('views.updateX2'))

#     return render_template('game.html', game=game)

# @views.route("/games/X2/update", methods = ["GET", "POST"])
# def updateX2():
#     gameToUpdate = Game.query.filter_by(id=2).first_or_404()
#     if request.method == "POST":
#         newTitle = request.form.get("title")
#         newPlatforms = request.form.get("platforms")
#         newSeries = request.form.get("series")
#         newFranchise = request.form.get("franchise")
#         newGenre1 = request.form.get("genre1")
#         newGenre2 = request.form.get("genre2")
#         newGenre3 = request.form.get("genre3")
#         newRelease = request.form.get('releaseDate')
#         newDS = request.form.get('dateStarted')
#         newDF = request.form.get('dateFinished')
#         newDesc = request.form.get('description')
#         newScore = request.form.get('score')

#         # Check validity of inputs and flash messages
#         if len(newTitle) < 1:
#             flash("Title must be greater than 1 character.", category='error')
#         elif len(newPlatforms) < 1:
#             flash("Platforms entry must be at least 1 character.", category='error')
#         elif newGenre2 == newGenre1 or newGenre3 == newGenre1 or (newGenre2 == newGenre3 and newGenre2 != 'N/A'):
#             flash("Cannot have two of the same genre.", category='error')
#         elif newRelease == '':
#             flash('Must enter release date.', category='error')
#         elif newDS == '':
#             flash('Must enter date started.', category='error')
#         elif len(newDesc) > 5000:
#             flash('Description cannot be longer than 5000 characters.', category='error')
#         else:

#             # Convert html dates to Python dates
#             newRelease = datetime.strptime(newRelease, '%Y-%m-%d')
#             newRelease = newRelease.date()
#             newDS = datetime.strptime(newDS, '%Y-%m-%d')
#             newDS = newDS.date()
#             newDF = datetime.strptime(newDF, '%Y-%m-%d')
#             newDF = newDF.date()

#             # Convert blanks to None (NULL in db)
#             if newSeries == '':
#                 newSeries = None
#             if newFranchise == '':
#                 newFranchise == None
#             if newGenre2 == 'N/A':
#                 newGenre2 = None
#             if newGenre3 == 'N/A':
#                 newGenre3 = None


#             # Update values
#             gameToUpdate.title = newTitle
#             gameToUpdate.platforms = newPlatforms
#             gameToUpdate.series = newSeries
#             gameToUpdate.franchise = newFranchise
#             gameToUpdate.genre1 = newGenre1
#             gameToUpdate.genre2 = newGenre2
#             gameToUpdate.genre3 = newGenre3
#             gameToUpdate.releaseDate = newRelease
#             gameToUpdate.dateStarted = newDS
#             gameToUpdate.dateFinished = newDF
#             gameToUpdate.description = newDesc
#             gameToUpdate.score = newScore

#             # Check if game cover or music has been updated, skip if not
#             newGameCoverName = ''
#             newGameMusicName = ''
#             if request.files.get('gameCover') and request.files.get('gameCover').filename != gameToUpdate.gameCover:
#                 newGameCoverName = request.files.get('gameCover').filename
#                 newGameCoverName = secure_filename(newGameCoverName)
#                 newGameCoverName = str(uuid.uuid1()) + "_" + newGameCoverName
#                 gameToUpdate.gameCover = newGameCoverName

#             if request.files.get('gameMusic') and request.files.get('gameMusic').filename != gameToUpdate.gameMusic:
#                 newGameMusicName = request.files.get('gameMusic').filename
#                 newGameMusicName = secure_filename(newGameMusicName)
#                 newGameMusicName = str(uuid.uuid1()) + "_" + newGameMusicName
#                 gameToUpdate.gameMusic = newGameMusicName        

#             # Save new files
#             try:
#                 if newGameCoverName != '':
#                     request.files.get('gameCover').save(os.path.join(current_app.config["UPLOAD_FOLDER"], newGameCoverName))
#                 if newGameMusicName != '':
#                     request.files.get('gameMusic').save(os.path.join(current_app.config["UPLOAD_FOLDER"], newGameMusicName))

#                 db.session.commit()
#                 flash("Success!", category="success")
#                 return redirect(url_for('views.game', title=gameToUpdate.title))
#             except:
#                 flash("Error", category="error")

#     return render_template('update_game.html', game=gameToUpdate)