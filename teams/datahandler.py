import sqlite3
import settings
import pprint

db_file = settings.db_file

def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        #Create Table "teams"
        cur.execute('''
                CREATE TABLE IF NOT EXISTS "teams" (
                    "id"	INTEGER NOT NULL,
                    "name"	VARCHAR(100) NOT NULL UNIQUE,
                    "group"	INTEGER NOT NULL DEFAULT 0,
                    "contactPerson"	VARCHAR(300),
                    "mobile"	VARCHAR(300),
                    PRIMARY KEY("id")
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
                        "group":row[2],
                        "contactPerson":row[3],
                        "mobile":row[4],
                })

        con.close()
        return list


def add_Team(name, group, contactPerson=None, mobile=None):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        try:
                cur.execute("INSERT INTO teams(name, group, contactPerson, mobile) VALUES (?,?,?)", (name, group, contactPerson, mobile))
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