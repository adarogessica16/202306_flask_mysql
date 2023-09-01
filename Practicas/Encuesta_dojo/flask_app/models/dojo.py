import os
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Dojo:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name= data['name']
        self.location= data['location']
        self.language = data['language']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod 
    def get_all(cls):
        resultados_instancias = []
        query = "SELECT * FROM dojos"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias
    #Obtener el ultimo dojo
    @classmethod
    def get(cls):
        query = "SELECT * FROM dojos ORDER BY dojos.id DESC LIMIT 1;"
        resultados = connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db( query)
        if resultados:
            return cls(resultados[0])
        else:
            return None

    @staticmethod
    def validar(dojo):
        is_valid = True
        if len(dojo['name']) < 3:
            flash(f"Debe rellenar este campo", "info")
            is_valid = False
        if len(dojo['location']) < 1:
            flash(f"Debe seleccionar una ubicacion", "info")
            is_valid = False
        if len(dojo['language']) < 1:
            flash(f"Elija un lenguaje favorito", "info")
            is_valid = False
        if len(dojo['comment']) < 5:
            flash(f"Haga un comentario mas largo..","info")
            is_valid = False
        return is_valid
    

    @classmethod #para guardar los datos de los users
    def save(cls, data ):
        query = "INSERT INTO dojos (name, location,language, comment, created_at, updated_at) VALUES (%(name)s, %(location)s, %(language)s, %(comment)s, NOW(), NOW() );" #reminder: now() me da la fecha y hora exacta de cuando se inserta
        return connectToMySQL(os.getenv('BASE_DE_DATOS')).query_db( query, data )
    