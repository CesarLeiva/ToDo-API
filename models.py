class User:
    def __init__(self, account, password, name=None) -> None:
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

class Task:
    def __init__(self, user_id, description, priority=None, date=None, time=None, completed = False, published = False, id=None):
        self._user_id = user_id
        self._description = description
        self.priority = priority
        # date=2024-08-06&time=14:45
        self.date = date
        self.time = time
        # priority_list = ['high', 'medium', 'low', 'very low']
        self.completed = completed
        self.published = published
        self._id = id

    @property
    def user_id(self) -> str:
            return self._user_id
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def id(self) -> str:
            return self._id
    
    def setid(self, id) -> set:
        self._id = id
    
    def setdescription(self, description) -> set:
        self._description = description
    
    def serialize(self) -> dict:
        return {
            "id": self._id,
            "description": self._description,
            "priority": self.priority,
            "date": self.date,
            "time": self.time,
            "completed": self.completed,
            "published": self.published
        }
    
    

class Super_task(Task):
    def __init__(self, user_id, description):
        super().__init__(user_id, description)
    
class Sub_task(Task):
    def __init__(self, super_task_id, description, priority=None, date=None, time=None):
        super().__init__(id, description, priority, date, time)
        self.super_task_id = super_task_id