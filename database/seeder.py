import sqlite3 as sql
import bcrypt

db_path = "C:\\Users\\César Leiva\\Desktop\\ToDo-API\\database\\ToDo.db"

def create_db():
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account UNIQUE NOT NULL,
        password NOT NULL,
        name TEXT NOT NULL        
        )"""
    )
    cursor.execute(
        """CREATE TABLE tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE,
        published BOOLEAN DEFAULT FALSE,
        priority TEXT,
        date DATE,
        time TIME,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
    )
    cursor.execute(
        """CREATE TABLE super_tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
    )
    cursor.execute(
        """CREATE TABLE sub_tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        super_task_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE,
        published BOOLEAN DEFAULT FALSE,
        priority TEXT,
        date DATE,
        time TIME,
        FOREIGN KEY (super_task_id) REFERENCES super_tasks(id)
        )"""
    )
    conn.commit()
    conn.close()

def get_id(account): #! Obtener el id de la cuenta loggeada
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE account = ?", (account,))
    id = cursor.fetchone()[0]
    conn.close()
    return id

def create_user(user) -> bool: #! Función registro de usuario
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE account = ?", (user.account,))

    if cursor.fetchone(): # Si el usuario existe
        conn.close()
        return False
    
    else: # Si el usuario no existe
        cursor.execute(
            """INSERT INTO users (account, password, name)
            VALUES(?, ?, ?)""",
            (user.account, hashed_password, user.name)
        )
        conn.commit()
        conn.close()
        return True

def log_in(user): #! Función inicio de sesión 
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE account = ?", (user.account,))
    result = cursor.fetchone()
    if result:
        stored_password = result[0]
        if bcrypt.checkpw(user.password.encode('utf-8'), stored_password):
            conn.close()
            return True
    else:
        conn.close()
        return False

def show_tasks(user_id): #! Mostrar tareas creadas por el usuario
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM tasks WHERE user_id = ?", str(user_id))
    tasks = cursor.fetchall()
    if tasks:
        return tasks
    else:
        return False

def create_task(task): #! Crear una tarea
    # ToDo: Evitar que se guarde "" en vez de null
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tasks (user_id, description, completed, published, priority, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (task.user_id, task.description, task.completed, task.published, task.priority, task.date, task.time)
    )
    conn.commit()
    conn.close()

def complete_task(): #ToDo: Marcar tarea como completada
    pass

if __name__ == '__main__':
    create_db()