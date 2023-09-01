from flask_app import app
from flask import render_template,redirect,request,flash
from flask_app.models.dojo import Dojo

@app.route('/')
def index():
    return render_template("form.html")


@app.route('/process', methods=['POST'])
def process():
        print(request.form)
        if Dojo.validar(request.form):
            Dojo.save(request.form)
            flash(f"Añadiste una nueva informacion", "success")
            return redirect("/result")
        flash(f"Por favor complete todos los campos", "info")
        return redirect("/")


@app.route("/result")
def result():
    dojo=Dojo.get()
    return render_template("info.html", dojo=dojo)