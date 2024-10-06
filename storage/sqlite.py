import sqlite3

from .base import Storage

class User:
    pass

class CheckIn:
    pass

class SQLiteStorage(Storage):
    def __init__(self, config={}):

        print(config)
        self.db_path = config['db_path'] 
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS check_in (id INTEGER PRIMARY KEY, user_id INTEGER, timestamp INTEGER, date TEXT, payload TEXT)")
        self.conn.commit()

    def add_user(self, user: User):
        self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email))
        self.conn.commit()

    def get_user(self, user_id: int) -> User:
        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row[1], row[2])
        return None
    
    def add_check_in(self, check_in: CheckIn):
        self.cursor.execute("INSERT INTO check_in (user_id, timestamp, date)")
        self.conn.commit()

    def close(self):
        self.conn.close()