from flask_app import app
from flask import redirect, render_template,request
from ..models.author import Author
from ..models.book import Book


@app.route('/books')
def books():
    all_books= Book.get_all()
    return render_template('books.html',all_books=all_books)

@app.route('/process_newBook',methods=['POST'])
def new_book():
    data = {
        "title":request.form['title'],
        "num_of_pages": request.form['num_of_pages']
    }
    book_id = Book.add_book(data)
    return redirect('/books')

@app.route('/book/<int:id>')
def show_book(id):
    data = {
        "id":id
    }
    book= Book.get_by_id(data)
    no_favorito_author= Author.author_no_favorito(data)
    return render_template('book_Show.html',book=book,no_favorito_author=no_favorito_author)

@app.route('/join/author',methods=['POST'])
def join_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_favorite(data)
    return redirect(f"/book/{request.form['book_id']}")