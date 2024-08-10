import bcrypt

class User:
    def __init__(self, account, password, name) -> None:
        self._account = account
        self._password = password
        self._name = name
        self._id = None

    @property
    def account(self) -> str:
        return self._account
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def id(self) -> str:
        return self._id
    
    def setid(self, id) -> None:
        self._id = id

    def check_password(self, stored_password) -> bool:
        if stored_password and bcrypt.checkpw(self._password.encode('utf-8'), stored_password):
            print("Inicio de sesión exitoso")
            return True
        else:
            print("Usuario o contraseña incorrectos")
            return False

class Task:
    def __init__(self, user_id, description, priority=None, date=None, time=None):
        self.user_id = user_id
        self.description = description
        self.completed = False
        self.published = False
        # date=2024-08-06&time=14:45
        self.date = date
        self.time = time
        # priority_list = ['high', 'medium', 'low', 'very low']
        self.priority = priority
        self.id = None

class Super_task(Task):
    def __init__(self, user_id, description):
        super().__init__(user_id, description)
    
class Sub_task(Task):
    def __init__(self, super_task_id, description, priority=None, date=None, time=None):
        super().__init__(id, description, priority, date, time)
        self.super_task_id = super_task_id