from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from models import User, Task
from database.seeder import create_user, log_in, show_tasks, get_id, create_task, complete_task, modify_task, delete_task
from logging import exception

app = Flask(__name__)
app.secret_key = "apikey"

# ToDo: Poner los códigos en los return jsonify() 

#*----------------------------------------------------------------------------------------------*#
#? Rutas para mostrar renders

@app.route('/') #! Muestra el formulario para loggearse
def loginpage():
    return render_template("login.html")

@app.route('/register') #! Muestra el html para registrarse
def register():
    return render_template("register.html")

@app.route('/menu') #! Muestra las tareas del usuario
def menu():
    try:
        if 'account_id' in session:
            return render_template("menu.html")
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/addtask') #! Muestra el formulario para agregar una nueva tarea
def addtaskpage():
    try:
        if 'account_id' in session:
            return render_template("addtask.html")
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/modifytask') #! Muestra el formulario para modificar la información de una tarea
def modify_task_page():
    try:
        if 'account_id' in session:
            return render_template("modifytask.html")
        else:
            return jsonify({'msg': "there is'n active session"}), 404
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
            session['account_id'] = get_id(user.account)
            return redirect(url_for("menu"))
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
            session['account_id'] = get_id(user.account) #? Guarda el id del usuario como variable de sesión
            return redirect(url_for('menu'))
        else:
            return jsonify({"msg": "wrong username or password"}), 200
    except Exception:
        exception("\n[SERVER]: error in rourte /api/login. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/logout') #! Logout
def logout():
    try:
        if 'account_id' in session:
            session.pop('account_id') #? Elimina la variable de la sesión
            print("session was deleted")
            return redirect(url_for('loginpage')) #? Sirve para redireccionar a una función con app.route
        else:
            return jsonify({'msg': "there is'n active session"}), 404        
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

#*----------------------------------------------------------------------------------------------*#
#? Rutas para gestionar las tareas

@app.route('/api/showtasks', methods=["GET"]) #! Mostrar todas las tareas del usuario
def showtasks():
    try:
        if 'account_id' in session:
            if show_tasks(session['account_id']):
                task_list = []
                for task in show_tasks(session['account_id']):
                    task_serializated = Task(id=int(task[0]), user_id=int(task[1]), description=task[2],
                                            completed=bool(task[3]), published=bool(task[4]),
                                            priority=task[5], date=task[6], time=task[7]).serialize()
                    task_list.append(task_serializated)
                return jsonify(task_list)
            else:
                return jsonify({"msg": "there are no tasks created"})
        else:
            return jsonify({'msg': "there is'n active session"}), 404

    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/addtask', methods=["POST"]) #! Crear tarea
def addtask():
    try:
        if 'account_id' in session:
            user_id=session['account_id']
            description=request.form['description']
            priority=request.form['priority'] if not "" else None
            date=request.form['date'] if not "" else None
            time=request.form['time'] if not "" else None
            new_task = Task(user_id=user_id, description=description, priority=priority, date=date, time=time)
            create_task(new_task)
            return jsonify({"msg": "new task was created"})
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/completetask', methods=["POST"]) #! Marcar tarea como completada
def completetask():
    try:
        if 'account_id' in session:
            if complete_task(user_id=session['account_id'], task_id=request.form['task_id']):
                return jsonify({'msg': "completed status was changed"})
            else:
                return jsonify({'msg': "task doesn't exist"})
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/modifytask', methods=["POST"]) #! Editar valores de una tarea
def modifytask():
    try:
        if 'account_id' in session:
            description = request.form['description']
            priority = request.form['priority']
            time = request.form['time']
            date = request.form['date']
            task_id = request.form['task_id']
            task_modify = Task(user_id=session['account_id'], description=description, priority=priority, time=time, date=date, id=task_id)
            if modify_task(task_modify):
                return jsonify({"msg": "task successfully modified"})
            else:
                return jsonify({"msg": "task doesn't exist"})
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/deletetask', methods=["POST"]) #! Eliminar una tarea
def deletetask():
    try:
        if 'account_id' in session:
            if delete_task(request.form['task_id'], session['account_id']):
                return jsonify({"msg": "task deleted successfully"})
            else:
                return jsonify({"msg": "task doesn't exist"})
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/register. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=4000)