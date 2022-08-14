import datetime
import sqlite3
import settings
from passlib.hash import sha256_crypt
import sys

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
                permission INTEGER NOT NULL,
                last_login TIMESTAMP
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
                cur.execute("INSERT INTO users (username, password, permission, email) VALUES (?, ?, ?, ?)", (username, hash, permission, email))
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
                        updateLastLogin(username)
                        return True, data[4]
                else:
                        return False, 0
        else:
                return False, 0


def updateLastLogin(username):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        try:
                now = datetime.datetime.now().timestamp()
                data = cur.execute("UPDATE users SET last_login = ? WHERE username = ?",[now, username]).fetchall()
                con.commit()
        except Exception as e:
                print(e)


def getUsers():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM users ORDER BY username ASC')
        for row in result:
                if row[5]:
                        last_login = datetime.datetime.fromtimestamp(row[5]).strftime("%Y-%m-%d %H:%M:%S")
                else:
                        last_login = None
                list.append({
                        "id": row[0],
                        "username": row[1],
                        "email": row[3],
                        "permission": row[4],
                        "last_login": last_login,
                })

        con.close()
        return list

if __name__ == "__main__":
        init()
        if(sys.argv[1] and sys.argv[2]):
                name = sys.argv[1]
                pw = sys.argv[2]
                add_User(name, pw, 3)

                print("Created User")
                print("name : " + name)
                print("password : " + pw)
