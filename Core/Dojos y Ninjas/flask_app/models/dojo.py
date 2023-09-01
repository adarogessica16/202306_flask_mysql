from flask import flash, redirect, render_template, request, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.ninja import Ninja
class Dojo:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = [] 

    @classmethod
    def get_all(cls):
        dojos = []
        query = "SELECT * FROM dojos"
        resultados = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            dojos.append(instancia)

        return dojos
    @classmethod
    def add_dojo(cls, data):
        query = "INSERT INTO dojos (nombre, created_at, updated_at) VALUES (%(nombre)s, NOW(), NOW())"
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)
    
    @classmethod
    def get(cls, id):
        query = """
        SELECT *
        FROM dojos
        LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id
        WHERE dojos.id = %(id)s;
        """
        data = {'id': id}
        resultados = connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)
        if len(resultados) == 0:
            return None  # Manejar caso cuando no se encuentra el dojo

        instancia_dojo = cls(resultados[0])

        for registro in resultados:
            if registro['ninjas.id']:  # Verificar si hay datos de ninja en este registro
                data = {
                    'id': registro['ninjas.id'],
                    'first_name': registro['first_name'],
                    'last_name': registro['last_name'],
                    'age': registro['age'],
                    'created_at': registro['created_at'],
                    'updated_at': registro['updated_at'],
                    'dojo': instancia_dojo
                }
                instancia_ninja = Ninja(data)
                instancia_dojo.ninjas.append(instancia_ninja)

        return instancia_dojo