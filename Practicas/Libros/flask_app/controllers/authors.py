
from flask_app import app
from flask import redirect, render_template,request
from ..models.author import Author
from ..models.book import Book

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def authors():
    authors= Author.get_all()
    return render_template('authors.html',authors=authors)

@app.route('/process_newAuthor',methods=['POST'])
def newAuthor():
    data = {
        "name": request.form['name']
    }
    author_id = Author.add_author(data)
    return redirect('/authors')

@app.route('/author/<int:id>')
def show_author(id):
    data = {
        "id": id
    }
    author= Author.get_by_id(data)
    no_favoritos=Book.get_no_favoritos(data)
    print("Author:", author)
    print("No favoritos:", no_favoritos) 
    return render_template('author_Show.html',author=author,no_favoritos=no_favoritos)

@app.route('/join/book',methods=['POST'])
def join_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_favorite(data)
    return redirect(f"/author/{request.form['author_id']}")