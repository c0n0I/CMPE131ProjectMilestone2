from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from app.forms import LoginForm
from app.models import User
from . import auth_bp

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()

        user = User.query.filter_by(username=username).first()

        if user:
            login_user(user)
            return redirect(url_for("main.index"))
        else:
            flash("Username not found.", "error")

    return render_template("auth/login.html", form=form)

from flask_login import login_required, logout_user

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
