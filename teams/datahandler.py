import sqlite3
import settings
import pprint

db_file = settings.db_file

def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        #Create Table "teams"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                contactPerson VARCHAR(300),
                email VARCHAR(300)
            );
        ''')

def get_Teams():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM teams ORDER BY name ASC')
        for row in result:
                list.append({
                        "id":row[0],
                        "name":row[1],
                        "contactPerson":row[2],
                        "email":row[3],
                })

        con.close()
        return list


def add_Team(name, contactPerson=None, email=None):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        try:
                cur.execute("INSERT INTO teams(name, contactPerson, email) VALUES (?,?,?)", (name, contactPerson, email))
        except Exception as e:
                print(e)
        con.commit()
        con.close()


def delete_Team(id):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        cur.execute("DELETE FROM order_history WHERE team_id=?", (id,))
        cur.execute("DELETE FROM teams WHERE id=?", (id,))

        con.commit()
        con.close()