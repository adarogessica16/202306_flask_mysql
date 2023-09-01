import os
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
class Book:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.favoritos = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        books = []
        query = "SELECT * FROM books"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            books.append(instancia)

        return books
    @classmethod
    def add_book(cls, data):
        query = "INSERT INTO books (title,num_of_pages, created_at, updated_at) VALUES (%(title)s,%(num_of_pages)s, NOW(), NOW())"
        return connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query, data)
    
    @classmethod
    #Obtener un libro por id
    def get_author(cls, data):
        books = []
        query = """SELECT * FROM books WHERE id = %(id)s"""
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query, data)
        for resultado in resultados:
            instancia = cls(resultado)
            books.append(instancia)
        return books
    
    @classmethod
    #Obtener por id un libro con los autores que lo marcan como favorito
    
    def get_by_id(cls,data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query,data)

        book = cls(resultados[0])

        for resultado in resultados:
            if resultado['authors.id'] == None:
                break
            data = {
                "id": resultado['authors.id'],
                "name": resultado['name'],
                "created_at": resultado['authors.created_at'],
                "updated_at": resultado['authors.updated_at']
            }
            book.favoritos.append(author.Author(data))
        return book
    
    #Retorna los libros no marcados como favoritos
    @classmethod
    def get_no_favoritos(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query, data)
        books = []
        for resultado in resultados:
            instancia = cls(resultado)  
            books.append(instancia)
            print(books)
        return books