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

def create_user(user) -> bool: #! Función registro de usuario
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE account = ?", (user.account,))

    if cursor.fetchone(): # Si el usuario existe
        conn.close()
        print("usuario existente")
        return False
    
    else: # Si el usuario no existe
        cursor.execute(
            """INSERT INTO users (account, password, name)
            VALUES(?, ?, ?)""",
            (user.account, hashed_password, user.name)
        )
        conn.commit()
        conn.close()
        print("usuario creado con éxito")
        return True

def log_in(user): #! Función inicio de sesión
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE account = ?", (user.account,))
    return user.check_password(cursor.fetchone()[0])

def log_out():
    pass

def create_task():
    pass

def create_super_task():
    pass

def create_sub_task():
    pass

def complete_task():
    pass

def complete_sub_task():
    pass

if __name__ == '__main__':
    create_db()