from flask import (render_template, request, redirect, url_for,
                   make_response,
                   session,
                   flash,
                   )
from . import user_bp


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


@user_bp.route("/profile")
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
    if "username" in session:
        return redirect(url_for("users.get_profile"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin":
            session["username"] = username
            flash("Login successful", "success")
            return redirect(url_for("users.get_profile"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("users/login.html")


@user_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out", "success")
    return redirect(url_for("users.login"))
