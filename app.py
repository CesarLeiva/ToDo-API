from flask import Flask, jsonify, request, session
from models import User, Task
from database.seeder import create_user, log_in, show_tasks, get_id, create_task, complete_task, modify_task, delete_task, find_tasks
from logging import exception
import re

app = Flask(__name__)
app.secret_key = "apikey"

#ToDo: Hacer buscadores por los diferentes parámestros

#*----------------------------------------------------------------------------------------------*#
#? Rutas para gestionar al usuario - sign up, log in y log out

@app.route('/api/signup', methods=['POST']) #! Registrar usuario
def signup():
    try:
        account = request.form['account']
        password = request.form['password']
        name = request.form['name']
        if account and password and name:
            user = User(account=account, password=password, name=name)
            if create_user(user):
                session['account_id'] = get_id(user.account)
                return jsonify({"msg": "successfully registered"}), 201
            else:
                return jsonify({"msg": "existing user"}), 409
        else:
            return jsonify({"msg": "parameters are missing"}), 400
    except Exception:
        exception("\n[SERVER]: error in rourte /api/signup. Log: \n")
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/login', methods=["POST"]) #! Iniciar sesión
def login():
    try:
        account = request.form["account"]
        password = request.form["password"]
        if account and password:
            user = User(account=account, password=password)
            if log_in(user):
                session['account_id'] = get_id(user.account)
                return jsonify({"msg": "session successfully started"}), 200
            else:
                return jsonify({"msg": "wrong username or password"}), 401
        else:
            return jsonify({"msg": "parameters are missing"}), 400
    except Exception:
        exception("\n[SERVER]: error in rourte /api/login. Log: \n")
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/logout') #! Logout
def logout():
    try:
        if 'account_id' in session:
            session.pop('account_id')
            return jsonify({'msg': "session was deleted"}), 200
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/logout. Log: \n")
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
                return jsonify(task_list), 200
            else:
                return jsonify({"msg": "there are no tasks created"}), 200
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/showtasks. Log: \n")
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/addtask', methods=["POST"]) #! Crear tarea
def addtask(): 
    try:
        if 'account_id' in session:
            user_id=session['account_id']
            description=request.form['description']
            priority=request.form['priority']
            date=request.form['date']
            time=request.form['time']
            priority_list = ["high", "medium", "low", "very low", ""]
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            time_pattern = r'^\d{2}:\d{2}$'
            if not description:
                return jsonify({"msg": "Error. No description was provided"}), 400
            elif priority not in priority_list:
                return jsonify({"msg": "Error. The accepted priority strings are '' or 'high', 'medium', 'low', 'very low'"}), 400
            elif date != "" and not re.match(date_pattern, date):
                return jsonify({"msg": "Error. The date parameter only accepts strings '' or in the format 'YYYY-MM-DD'"}), 400
            elif time != "" and not re.match(time_pattern, time):
                return jsonify({"msg": "Error. The time parameter only accepts strings '' or in the format 'HH:MM'"}), 400
            else:
                new_task = Task(user_id=user_id, description=description, priority=priority, date=date, time=time)
                create_task(new_task)
                return jsonify({"msg": "new task was created"}), 201
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/addtask. Log: \n") # devueve error si algo sale mal (por consola)
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/completetask', methods=["PUT"]) #! Marcar tarea como completada
def completetask():
    try:
        if 'account_id' in session:
            if complete_task(user_id=session['account_id'], task_id=request.args['task_id']):
                return jsonify({'msg': "completed status was changed"}), 200
            else:
                return jsonify({'msg': "task doesn't exist"}), 404
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/completetask. Log: \n")
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/modifytask', methods=["PUT"]) #! Editar valores de una tarea
def modifytask():
    try:
        if 'account_id' in session:
            user_id=session['account_id']
            task_id=request.form['task_id']
            description=request.form['description']
            priority=request.form['priority']
            date=request.form['date']
            time=request.form['time']
            priority_list = ["high", "medium", "low", "very low", ""]
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            time_pattern = r'^\d{2}:\d{2}$'
            if description == "":
                return jsonify({"msg": "Error. No description was provided"}), 400
            elif task_id == "":
                return jsonify({"msg": "Error. No task id was provided"}), 400
            elif priority not in priority_list:
                return jsonify({"msg": "Error. The accepted priority strings are '' or 'high', 'medium', 'low', 'very low'"}), 400
            elif date != "" and not re.match(date_pattern, date):
                return jsonify({"msg": "Error. The date parameter only accepts strings '' or in the format 'YYYY-MM-DD'"}), 400
            elif time != "" and not re.match(time_pattern, time):
                return jsonify({"msg": "Error. The time parameter only accepts strings '' or in the format 'HH:MM'"}), 400
            else:
                task_modify = Task(user_id=user_id, description=description, priority=priority, time=time, date=date, id=task_id)
                if modify_task(task_modify):
                    return jsonify({"msg": "task successfully modified"}), 200
                else:
                    return jsonify({"msg": "task doesn't exist"}), 404
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/modifytask. Log: \n")
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/deletetask', methods=["DELETE"]) #! Eliminar una tarea
def deletetask():
    try:
        if 'account_id' in session:
            if delete_task(request.args['task_id'], session['account_id']):
                return jsonify({"msg": "task deleted successfully"}), 200
            else:
                return jsonify({"msg": "task doesn't exist"}), 404
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/deletetask. Log: \n")
        return jsonify({"msg": "An error has occurred"}), 500

@app.route('/api/findtasks', methods=["GET"]) #! Buscar tareas
def findtasks():
    try:
        description = request.args['description']
        if 'account_id' in session:
            if show_tasks(session['account_id']):
                task_list = []
                for task in find_tasks(f"%{description}%"):
                    task_serializated = Task(id=int(task[0]), user_id=int(task[1]), description=task[2],
                                            completed=bool(task[3]), published=bool(task[4]),
                                            priority=task[5], date=task[6], time=task[7]).serialize()
                    task_list.append(task_serializated)
                return jsonify(task_list), 200
            else:
                return jsonify({"msg": "there are no tasks that match that search"}), 404
        else:
            return jsonify({'msg': "there is'n active session"}), 404
    except Exception:
        exception("\n[SERVER]: error in rourte /api/findtasks. Log: \n")
        return jsonify({"msg": "An error has occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=4000)