from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Link, User
from .form import RegisterForm, LoginForm
from .extensions import db
from flask_login import login_user, logout_user, login_required, current_user


shortener = Blueprint('shortener', __name__)

@shortener.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.views = link.views + 1
    db.session.commit()
    return redirect(link.original_url)

@shortener.route('/create_link', methods=["POST"])
def create_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()
    
    return render_template('link_success.html', new_url=link.short_url, original_url=link.original_url)

@shortener.route('/')
def index():
    return render_template("index.html")

@shortener.route('/analytics')
def analytics():
    links = Link.query.all()
    
    return render_template('analytics.html',links=links)

@shortener.errorhandler(404)
def page_not_found(e):
    return "<h1>Page Not Found, 404<h1/>", 404,


@shortener.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}",
            category="success",
        )
        return redirect(url_for("create_link"))
    if form.errors != {}:  # if there are no errors in the validations
        for err_msg in form.errors.values():  # when there are errors in validations
            flash(
                f"There was an error with creating a user: {err_msg}", category="danger"
            )
    return render_template("register.html", form=form)


@shortener.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Success! You are logged in as {attempted_user.username}",
                category="success",
            )
            return redirect(url_for("create_link"))
        else:
            flash(
                "Username and password are not match! Please try again",
                category="danger",
            )

    return render_template("login.html", form=form)


@shortener.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("index"))