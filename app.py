from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from models import User, Task
from database.seeder import create_user, log_in
from logging import exception

app = Flask(__name__)
app.secret_key = "cesar"

user = User("cesaracount", "contraseña", "César")

# Rutas
@app.route('/') # Index
def index():
    session['account'] = user.account #? Guarda una variable en la sesión
    if 'account' in session:
        account = session['user']
        print(account)
    return render_template("index.html")

@app.route('/api/login', methods=["POST"]) # Index
def login():
    try:
        user = User(request.form["account"], request.form["password"], request.form["name"])
        if log_in(user):
            session['account'] = user.account #? Guarda una variable en la sesión
            return jsonify({"msg": f"session started - {user.account}"}), 200
        else:
            return jsonify({"msg": "wrong username or password"}), 200
        # if 'account' in session:
        #     account = session['user']
        #     print(account)
    except Exception:
        exception("\n[SERVER]: error in rourte /api/login. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/logout') # Logout
def logout():
    if 'account' in session:
        session.pop('account') #? Elimina la variable de la sesión
        print("session was deleted")
    return redirect(url_for('prueba')) #? Sirve para redireccionar a una función con app.route

@app.route('/prueba') # prueba
def prueba():
    if 'account' in session:
        print("in session")
    else:
        print("no session")
    return render_template("index.html")


# create_user(user) #*Funciona
# log_in(user) #*Funciona





if __name__ == "__main__":
    app.run(debug=True, port=4000)