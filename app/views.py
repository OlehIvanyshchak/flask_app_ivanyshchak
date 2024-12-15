from flask import render_template, request, current_app


@current_app.route("/")
def main():
    return render_template("hello.html")


@current_app.route("/homepage")
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent
    return render_template("home.html", agent=agent)


@current_app.route("/resume")
def resume():
    return render_template("resume.html", title="Моє резюме")


@current_app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
