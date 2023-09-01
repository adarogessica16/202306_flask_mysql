
from flask_app import app
from flask import render_template, redirect, request, flash

from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo


@app.route("/ninjas")
def ninjas():
    dojos = Dojo.get_all()
    return render_template("newNinja.html", dojos= dojos)

@app.route("/ninjas/crear_ninja", methods=["POST"])
def add_ninja():
    
    data = {
        "dojo_id": request.form['dojo_id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "age": request.form['age']
    }
    
    Ninja.add_ninja(data)
    
    return redirect("/dojos")

