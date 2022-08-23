import sqlite3
import settings
from pprint import pprint

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
                group_id INTEGER,
                editor VARCHAR(100)
            );
        ''')

        #Create Table "item_groups"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS item_groups (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                color VARCHAR(32),
                editor VARCHAR(100)
            );
        ''')

        con.commit()
        con.close()

def get_Items(asGroup = False):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        groups = getGroups(asDic=True)

        list = []
        result = cur.execute('SELECT * FROM items ORDER BY group_id, name ASC')

        if asGroup:
                dic = {}
                for group in groups:
                        dic[groups[group]["id"]] = groups[group]
                        dic[groups[group]["id"]]["items"] = []

                for row in result:
                        print(row)
                        if row[3]:
                                group_id = row[3]
                        else:
                                group_id = 1

                        id = row[0]
                        name = row[1]
                        price = float(row[2])
                        group = groups[group_id]
                        editor = row[4]

                        dic[group_id]["items"].append({
                                "id" : row[0],
                                "name" : row[1],
                                "price" : float(row[2]),
                                "group" : groups[group_id],
                                "editor" : row[4]
                        })

                con.close()
                pprint(dic)
                return dic


        else:
                try:
                        for row in result:
                                if row[3]:
                                        group_id = row[3]
                                else:
                                        group_id = 1

                                list.append({
                                        "id" : row[0],
                                        "name" : row[1],
                                        "price" : float(row[2]),
                                        "group" : groups[group_id],
                                        "editor" : row[4]
                                })
                except Exception as e:
                        print(e)

                con.close()
                pprint(list)
                return list


def addItem(name, price=None, editor=None, group_id=1):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        try:
                cur.execute("INSERT INTO items(name, price, group_id, editor) VALUES (?,?,?,?)", (name, price, group_id, editor))
        except Exception as e:
                print(e)
        con.commit()
        con.close()


def getGroups(asDic = False):
        if asDic:
                con = sqlite3.connect(db_file)
                cur = con.cursor()

                result = cur.execute('SELECT * FROM item_groups ORDER BY id ASC')

                dic = {}
                try:
                        for row in result:
                                id = row[0]
                                name = row[1]
                                color = row[2]
                                editor = row[3]

                                dic[id] = {
                                        "id" : id,
                                        "name" : name,
                                        "color" : color,
                                        "editor" : editor,
                                }
                except Exception as e:
                       print(e)

                con.close()
                return dic

        else:
                con = sqlite3.connect(db_file)
                cur = con.cursor()

                result = cur.execute('SELECT * FROM item_groups ORDER BY name ASC')

                list = []
                try:
                        for row in result:
                                list.append({
                                        "id":row[0],
                                        "name":row[1],
                                        "color":row[2],
                                        "editor":row[3]
                                })
                except Exception as e:
                        print(e)

                con.close()
                return list


def addGroup(name, color="#5294ff", editor=None):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        try:
                cur.execute("INSERT INTO item_groups(name, color, editor) VALUES (?,?,?)", (name, color, editor))
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
