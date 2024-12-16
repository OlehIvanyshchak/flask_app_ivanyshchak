from flask import (render_template, request, redirect, url_for,
                   make_response,
                   session,
                   flash,
                   )
from . import user_bp
from app.users.models import User
from app import db
from app.users.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required


@user_bp.route("/hi/<string:name>")
def greeting(name):
    name = name.upper()
    age = request.args.get("age", 0, int)
    return render_template("users/hi.html", name=name, age=age)


@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greeting", age=45,
                     name="administrator", external=True)
    print(to_url)
    return redirect(to_url)


@user_bp.route("/set_cookie", methods=["GET", "POST"])
def set_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    max_age = request.form.get("max_age", 60, int)
    if not key or not value or not max_age:
        flash("Заповніть всі поля", "danger")
        return redirect(url_for("users.get_profile"))
    flash(f"Кука {key} зі значенням {value} встановлена", "success")
    response = make_response(redirect(url_for("users.get_profile")))
    response.set_cookie(key, value, max_age=max_age)
    return response


@user_bp.route("/get_cookie", methods=["GET", "POST"])
def get_cookie():
    username = request.cookies.get("username")
    return f"Користувач: {username}"


@user_bp.route("/delete_cookie", methods=["GET", "POST"])
def delete_cookie():
    key = request.form.get("key")
    flash(f"Кука {key} видалена", "success")
    response = make_response(redirect(url_for("users.get_profile")))
    response.delete_cookie(key)
    return response


@user_bp.route("/delete_all_cookies", methods=["GET", "POST"])
def delete_all_cookies():
    flash("Всі куки видалені", "success")
    response = make_response(redirect(url_for("users.get_profile")))
    for key in request.cookies:
        response.delete_cookie(key)
    return response


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in", "info")
        return redirect(url_for('users.get_account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User(username=form.username.data, email=email)
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@user_bp.route("/account", methods=["GET", "POST"])
@login_required
def get_account():
    all_users = User.query.all()
    user_count = len(all_users)
    return render_template(
        "users/account.html",
        user=current_user,
        all_users=all_users,
        user_count=user_count,
    )


@user_bp.route("/profile")
@login_required
def get_profile():
    if "username" in session:
        username = session["username"]
        return render_template(
            "users/profile.html", username=username, cookies=request.cookies
        )
    flash("You need to login", "danger")
    return redirect(url_for("users.login"))


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", "info")
        return redirect(url_for('users.get_account'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful", "success")
            return redirect(url_for('users.get_account'))
        flash("Invalid credentials", "danger")
    return render_template('users/login.html', form=form, title='Login')


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("users.login"))
