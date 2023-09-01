from flask import flash, redirect, render_template, request, session
from flask_app.config.mysqlconnection import connectToMySQL
class Usuario:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']

    @classmethod
    def get_all(cls):
        usuarios = []
        query = "SELECT * FROM usuarios"
        resultados = connectToMySQL('esquema_users').query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            usuarios.append(instancia)

        return usuarios
    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO usuarios (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW())"
        return connectToMySQL('esquema_users').query_db(query, data)

    
    @classmethod
    def get(cls, id ):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL('esquema_users').query_db( query, data )
        if resultados:
            return cls(resultados[0])
        return None
    
    @classmethod
    def update(cls,data):
        query = "UPDATE usuarios SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        data = {
            "id": int(data['id']),
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email']            
        } 
        return connectToMySQL('esquema_users').query_db(query,data)
    

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL('esquema_users').query_db(query,data)
        
    
    



