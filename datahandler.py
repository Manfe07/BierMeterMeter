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
        return list
        con.close()

if __name__ == "__main__":
        add_Beer("Team 3")