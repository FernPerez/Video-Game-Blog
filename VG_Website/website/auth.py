from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid as uuid
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #Check validity of inputs
        user = User.query.filter_by(email=email).first()
        usernameCheck = User.query.filter_by(username=username).first()

        if user:
            flash("Email is already registered. Please enter a different email.", category="error")
        elif usernameCheck:
            flash("Username is already taken.", category="error")
        elif len(email) <= 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(username) <= 4:
            flash("Username must be greater than 4 characters.", category='error')
        elif len(password1) <= 7:
            flash("Password must be greater than 7 characters.", category='error')
        elif password1 != password2:
            flash("Passwords do not match.", category='error')
        else:
            new_user = User(
                email = email,
                username = username,
                password = generate_password_hash(password1, method='sha256')
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User created!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            except:
                flash("Something went wrong...", category="error")


    return render_template("sign_up.html", user=current_user)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password! Try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", category="success")
    return redirect(url_for("auth.login"))