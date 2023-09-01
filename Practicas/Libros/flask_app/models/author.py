import os
from flask_app.config.mysqlconnection import connectToMySQL
from ..models import book
class Author:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.favorite_books = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        authors = []
        query = "SELECT * FROM authors"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            authors.append(instancia)

        return authors
    @classmethod
    def add_author(cls, data):
        query = "INSERT INTO authors (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW())"
        return connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query, data)
    #Inserta los favoritos
    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (author_id,book_id) VALUES (%(author_id)s,%(book_id)s);"
        return connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query,data)
    
    @classmethod
    def get_author(cls, data):
        query = "SELECT * FROM authors WHERE id = %(id)s"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query, data)
        authors = []
        for resultado in resultados:
            instancia = cls(resultado)  
            authors.append(instancia)
        return authors
    #Devuelve la lista de autores que no son marcados como favoritos
    @classmethod
    def author_no_favorito(cls,data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );"
        authors = []
        results = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query,data)
        for row in results:
            authors.append(cls(row)) 
        return authors
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query,data)
        author = cls(resultados[0])
        for resultado in resultados:
            if resultado['books.id'] == None:
                break
            data = {
                "id": resultado['books.id'],
                "title": resultado['title'],
                "num_of_pages": resultado['num_of_pages'],
                "created_at": resultado['books.created_at'],
                "updated_at": resultado['books.updated_at']
            }
            author.favorite_books.append(book.Book(data))
        return author