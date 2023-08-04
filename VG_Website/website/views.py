from flask import Blueprint, render_template, request, flash

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
        genre1 = request.form.get('genre1')
        genre2 = request.form.get('genre2')
        genre3 = request.form.get('genre3')
        releaseDate = request.form.get('releaseDate')
        dateStarted = request.form.get('dateStarted')
        dateFinished = request.form.get('dateFinished')
        description = request.form.get('description')
        score = request.form.get('score')
        gameCover = request.form.get('gameCover')

        if len(title) < 1:
            flash("Title must be greater than 1 character.", category='error')
        elif len(platforms) < 1:
            flash("Platforms entry must be at least 1 character.", category='error')
        elif genre2 == genre1 or genre3 == genre1 or (genre2 == genre3 and genre2 != "N/A"):
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
            flash('Game added!', category='success')


    return render_template("addGame.html")

@views.route("/games", methods=["GET"])
def games():
    return render_template("games.html")