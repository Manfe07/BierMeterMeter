import sqlite3
import settings
import pprint

db_file = settings.db_file

def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        #Create Table "items"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                price DECIMAL(5,2),
                editor VARCHAR(100)
            );
        ''')

        con.commit()
        con.close()

def get_Items():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM items ORDER BY name ASC')
        try:
                for row in result:
                        pprint.pprint(row)
                        list.append({
                                "id":row[0],
                                "name":row[1],
                                "price":float(row[2]),
                                "editor":row[3]
                        })
        except Exception as e:
                print(e)

        con.close()
        return list


def addItem(name, price=None, editor=None):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        try:
                cur.execute("INSERT INTO items(name, price, editor) VALUES (?,?,?)", (name, price, editor))
        except Exception as e:
                print(e)
        con.commit()
        con.close()

def deleteItem(id):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        cur.execute("DELETE FROM items WHERE id=?", (id,))

        con.commit()
        con.close()