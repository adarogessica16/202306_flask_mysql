
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuario import Usuario

@app.route('/')
def inicio():
    return render_template('leer.html',usuarios=Usuario.get_all())

@app.route('/usuario/new')
def new():
    return render_template("crear.html")

@app.route("/usuarios/show/<int:id>")
def show(id):
    usuario = Usuario.get(id)
    
    return render_template("usuario.html", usuario=usuario)

@app.route('/crear_usuario', methods=["POST"])
def crear_usuario():
    print("DATOS:", request.form)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    id = Usuario.add_user(data)

    flash(f"El usuario fue agregado exitosamente")
    return redirect('/')

@app.route('/user/edit/<int:id>')
def edit(id):
    usuario = Usuario.get(id)
    return render_template("edit.html", usuario=usuario)

@app.route('/user/update',methods=['POST'])
def update_user():
    data = {
        "id": request.form['id'],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    usuarios = Usuario.update(data)
    return redirect('/')

@app.route('/user/delete/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Usuario.delete(data)
    return redirect('/')