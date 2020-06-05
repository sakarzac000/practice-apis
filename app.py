from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)
heroku = Heroku(app)
CORS()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    review = db.Column(db.String(144), nullable=True)

    def __init__(self, title, author, review):
        self.title = title
        self.author = author
        self.review = review

class BookSchema(ma.Schema):
     class Meta:
        fields = ["id", "title", "author", "review"]

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route("/book/add", methods=['POST'])
def add_book():
    if request.content_type == "application/json":
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        review = post_data.get('review')

        record = Book(title, author, review)
        db.session.add(record)
        db.session.commit()

        return jsonify("Book Created")
    return jsonify("Request must be sent as JSON data")

@app.route('/book/get', methods=['GET'])
def get_all_books():
    all_books = db.session.query(Book).all()
    # books_json = []
    # for book in all_books:
    #     books_json.append({
    #         "id": book.id,
    #         "title": book.title,
    #         "author": book.author,
    #         "review": book.review
    #     })
    return jsonify(books_schema.dump(all_books))

if __name__ == "__main__":
    app.debug = True
    app.run()

