from flask import request, url_for, redirect, render_template
from . import app


@app.route("/")
def main():
    return "Hello, World!"


@app.route("/homepage")
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent
    return f"This is your Home page - {agent}"


@app.route("/user/<string:name>/<int:age>")
def greeting(name, age):
    name = name.upper()
    age = request.args.get("age", 0, int)
    return render_template("hi.html", name=name, age=age)


@app.route("/admin")
def admin():
    to_url = url_for("greeting", name="administrator", age=30, _external=True)
    print(to_url)
    return redirect(to_url)


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Моє резюме")


if __name__ == "__main__":
    app.run(debug=True)
