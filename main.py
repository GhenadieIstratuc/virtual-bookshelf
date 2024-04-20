from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


class Book(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float(200), nullable=False)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating


@app.route('/')
def home():
    return render_template('index.html', books=Book.query.all())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["name"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
