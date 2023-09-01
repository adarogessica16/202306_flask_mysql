from flask_app import app
from flask import render_template, redirect, request, flash

from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja
@app.route("/")
def inicio():
    return redirect("/dojos")

@app.route("/dojos")
def dojos():
    dojos = Dojo.get_all()   
    return render_template("dojos.html", dojos=dojos)


@app.route("/crear_dojo", methods=["POST"])
def add_dojo():
    
    data = {
        "nombre": request.form['nombre']
    }
    
    Dojo.add_dojo(data)
    
    return redirect("/dojos")
    
@app.route("/dojos/<int:id>/")
def get_dojo(id):
    dojo= Dojo.get(id)
    return render_template("show_dojo.html", dojo=dojo)
