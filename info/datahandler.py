import sqlite3
import settings
import pprint

db_file = settings.db_file

def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        #Create Table "infos"
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS infos (
                        id INTEGER PRIMARY KEY,
                        title char NOT NULL,
                        content TEXT NOT NULL,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

def get_Infos():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM infos ORDER BY timestamp desc')
        for row in result:
                list.append({
                        "id": row[0],
                        "title": row[1],
                        "content": row[2],
                        "Timestamp": row[3]
                })

        con.close()
        return list


def add_Info(title : str, content : str):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute("INSERT INTO infos(title, content) VALUES (?,?)", (title,content))

        con.commit()
        con.close()

def delete_Info(id):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute("DELETE FROM infos WHERE id=?", (id,))

        con.commit()
        con.close()