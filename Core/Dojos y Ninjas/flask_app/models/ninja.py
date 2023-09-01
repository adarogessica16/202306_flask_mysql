from flask import flash, redirect, render_template, request, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import dojo
class Ninja:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.dojo = data.get("dojo")
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    #Obtiene todos los datos
    def get_all(cls):
        ninjas = []
        query = "SELECT * FROM ninjas JOIN dojos ON ninjas.dojo_id= dojos.id"
        resultados = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            datos_dojo={
                'id':resultado['dojos.id'],
                'nombre': resultado['dojos.nombre'],
            }
            instancia_dojo= dojo.Dojo(datos_dojo)
            instancia.dojo= instancia_dojo
            ninjas.append(instancia)

        return ninjas
    @classmethod
    def add_ninja(cls, data):
        query = """INSERT INTO ninjas (first_name, last_name, age, dojo_id, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(age)s, %(dojo_id)s, NOW(), NOW())"""
        return connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)
    
    @classmethod
    def get_ninja(cls, data):
        ninjas = []
        query = """SELECT * FROM ninjas WHERE dojo_id = %(id)s"""
        resultados = connectToMySQL("esquema_dojos_y_ninjas").query_db(query, data)
        for resultado in resultados:
            instancia = cls(resultado)
            ninjas.append(instancia)
        return ninjas
