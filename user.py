import sqlite3
import settings
from passlib.hash import sha256_crypt

db_file = settings.db_file


def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        #Create Table "Users"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username VARCHAR(100) UNIQUE,
                password VARCHAR(200),
                email VARCHAR(200) UNIQUE,
                permission INTEGER NOT NULL
            );
        ''')

def check_User(username):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        data = cur.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if data:
                return True
        else:
                return False


def add_User(username, password, permission, email = None):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        hash = sha256_crypt.hash(password)
        if not check_User(username):
                if email:
                        cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hash, email))
                else:
                        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash))
                con.commit()
                con.close()
                return 1
        else:
                return -1       #-1 == User exists

def verify(username, password):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        if(check_User(username)):
                data = cur.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
                hash = data[2]
                if sha256_crypt.verify(password, hash):
                        return True, data[4]
                else:
                        return False, 0
        else:
                return False, 0

if __name__ == "__main__":
        init()
        add_User("test","test")
        print(verify("test","tests"))
        print(verify("test","test"))
        check_User("test")
