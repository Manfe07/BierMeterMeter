import sqlite3

db_file = 'bmm.db'

def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS biermeter (
                id INTEGER PRIMARY KEY,
                team TEXT NOT NULL,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
        ''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS infos (
                        id INTEGER PRIMARY KEY,
                        titel char NOT NULL,
                        content TEXT NOT NULL,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

        con.commit()
        con.close()


def beer(team : str, add : bool):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        if(add):
                cur.execute("INSERT INTO biermeter(team) VALUES (?)", (team,))
        elif(not add):
                timestamp = cur.execute("SELECT Timestamp FROM biermeter WHERE team=? ORDER BY Timestamp DESC LIMIT 1;", (team,)).fetchone()[0]
                cur.execute("DELETE FROM biermeter WHERE Timestamp=?", (timestamp,))
                print(timestamp)
        con.commit()
        con.close()


def get_List(ranking = False):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = None
        if ranking:
                result = cur.execute('SELECT team, count(*) FROM biermeter GROUP BY team ORDER BY count(*) DESC')
        else:
                result = cur.execute('SELECT team, count(*) FROM biermeter GROUP BY team ORDER BY team')
        for row in result:
                list.append({""
                             "team": row[0],
                             "amount" : row[1]
                             })
        con.close()
        return list

def get_Teams():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT name FROM teams ORDER BY name ASC')
        for row in result:
                list.append(row[0])

        con.close()
        return list

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




if __name__ == "__main__":
        beer("Team 3", True)