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





if __name__ == "__main__":
        init()