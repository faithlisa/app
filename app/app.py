from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

@app.route('/books')
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = Book(title=request.form['title'],
                        author=request.form['author'],
                        publication_year=request.form['year'])
        db.session.add(new_book)
        db.session.commit()
        return redirect('/books')
    return render_template('add_book.html')

# Create database and tables
def add_context():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    add_context()
    app.run(debug=True)
