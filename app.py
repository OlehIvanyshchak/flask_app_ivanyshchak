from flask import Flask, request, url_for, redirect, render_template, abort
app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def main():
    return "Hello, World!"


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent
    return f'This is your Home page - {agent}'


@app.route('/user/<string:name>/<int:age>')
def greeting(name, age):
    name = name.upper()
    age = request.args.get('age', 0, int)
    return render_template('hi.html', name=name, age=age)


@app.route('/admin')
def admin():
    to_url = url_for("greeting", name='administrator', age=30, _external=True)
    print(to_url)
    return redirect(to_url)


posts = [
    {"id": 1, 'title': 'My First Post',
        'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day',
        'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2',
        'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

@app.route('/posts')
def get_posts():
    return render_template("posts.html", posts=posts)
@app.route('/post/<int:id>')
def get_post(id):
    if id > len(posts):
        abort(404)
    post = posts[id-1]
    return render_template('detail-post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
