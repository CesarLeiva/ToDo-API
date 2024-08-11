from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from models import User, Task
from database.seeder import create_user, log_in
from logging import exception

app = Flask(__name__)
app.secret_key = "cesar"

# user = User("cesaracount", "contraseña", "César") #? Cuenta creada
# user = User("cuenta", "contraseña", "Nombre") #? Cuenta creada

#*----------------------------------------------------------------------------------------------*#
#? Rutas para mostrar renders

@app.route('/') #! Muestra el index para loggearse
def index():
    return render_template("login.html")

@app.route('/register') #! Muestra el html para registrarse
def register():
    return render_template("register.html")

@app.route('/menu') #! Muestra las tareas del usuario
def menu():
    try:
        if 'account' in session:
            return render_template("menu.html")
        else:
            return jsonify({'msg': "there is'n active session"})
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

#*----------------------------------------------------------------------------------------------*#
#? Rutas para gestionar al usuario - sign up, log in y log out

@app.route('/api/signup', methods=['POST']) #! Registrar usuario
def signup():
    try:
        user = User(request.form['account'], request.form['password'], request.form['name'])
        if create_user(user):
            return jsonify({"msg": "successfully registered"})
        else:
            return jsonify({"msg": "existing user"})
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/login', methods=["POST"]) #! Iniciar sesión
def login():
    try:
        user = User(request.form["account"], request.form["password"])
        if log_in(user):
            session['account'] = user.account #? Guarda una variable en la sesión
            return redirect(url_for('menu'))
        else:
            return jsonify({"msg": "wrong username or password"}), 200
    except Exception:
        exception("\n[SERVER]: error in rourte /api/login. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/logout') #! Logout
def logout():
    try:
        if 'account' in session:
            session.pop('account') #? Elimina la variable de la sesión
            print("session was deleted")
            return redirect(url_for('index'))
        # return redirect(url_for('log')) #? Sirve para redireccionar a una función con app.route
        else:
            return jsonify({'msg': "there is'n active session"})
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

#*----------------------------------------------------------------------------------------------*#
#? Rutas para gestionar las tareas

# todo: rutas

if __name__ == "__main__":
    app.run(debug=True, port=4000)