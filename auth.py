from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint(("auth"), __name__)

# logout, login and signup

@auth.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in in succesfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("password is incorerct", category="error")
        else:
            flash("E-mail is incorerct", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if (request.method == "POST"):
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password")
        password2 = request.form.get("password1")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if (email_exists):
            flash("Email is already in use,", category="error")
        elif (username_exists):
            flash("Username is already in use,", category="error")
        elif (password1 != password2):
            flash("Passwords do not match", category="error")
        elif len(username) < 2:
            flash("Username is too short", category="error")
        elif len(password1) < 7:
            flash("password needs to be of 7 characters", category="error")
        elif len(email) < 4:
            flash("email is invalid", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash("User created", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)

