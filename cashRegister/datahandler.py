import sqlite3
import settings
import pprint
import teams.datahandler as teamlist
db_file = settings.db_file

def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        #Create Table "order_history"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS order_history (
                id INTEGER PRIMARY KEY,
                team_id INTEGER NOT NULL,
                team_name VARCHAR(100) NOT NULL,
                item VARCHAR(100) NOT NULL,
                amount INTEGER NOT NULL,
                price DECIMAL(5,2),
                user_name VARCHAR(100),
                cash INTEGER,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        con.commit()
        con.close()


def get_List():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = None
        result = cur.execute('SELECT team_name, sum(amount) FROM order_history WHERE item="Biermeter" GROUP BY team_name ORDER BY sum(amount) DESC')
        for row in result:
                list.append({""
                             "team": row[0],
                             "amount" : row[1]
                             })
        con.close()
        return list


def add_Order(_data : dict):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        user_name = _data["user"]
        team_id = _data["team_id"]
        team_name = _data["team_name"]
        cash = _data["cash"]
        basket = _data["basket"]
        for item in basket:
                cur.execute("INSERT INTO order_history(team_id, team_name, item, amount, price, user_name, cash) VALUES (?,?,?,?,?,?,?)",
                            (team_id, team_name, basket[item]["name"], basket[item]["amount"], basket[item]["sum"], user_name, cash))
        con.commit()
        con.close()

def get_OrderHistory():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM order_history ORDER BY id DESC')
        for row in result:
                list.append({
                        "id":row[0],
                        "team_name":row[2],
                        "item":row[3],
                        "amount": row[4],
                        "sum": row[5],
                        "user": row[6],
                        "cash": row[7],
                        "timestamp": row[8],
                })
        con.close()
        return list


def delete_Order(id):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute("DELETE FROM order_history WHERE id=?", (id,))

        con.commit()
        con.close()

def get_TeamBills(cash_filter = False, cash = False):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        con = sqlite3.connect(db_file)
        cur = con.cursor()

        team_bill={}
        teams = teamlist.get_Teams()
        teams.append({
                "id": -1,
                "name": "Ohne Team",
                "contactPerson": None,
                "email": None,
        })
        for team in teams:
                list = []
                if not(cash_filter):
                        result = cur.execute(
                                "SELECT `item`, sum(`amount`), sum(`price`) FROM `order_history` WHERE `team_name`=? GROUP BY `item` ORDER BY `item` DESC",
                                (team["name"],))
                        for row in result:
                                list.append({
                                        "item": row[0],
                                        "amount": row[1],
                                        "sum": row[2]
                                })

                else:
                        result = cur.execute(
                                "SELECT `item`, sum(`amount`), sum(`price`), `cash` FROM `order_history` WHERE `team_name`=? GROUP BY `item`, `cash` ORDER BY `item` DESC",
                                (team["name"],))

                        for row in result:
                                list.append({
                                        "item": row[0],
                                        "amount": row[1],
                                        "sum": row[2],
                                        "cash": row[3]
                                })
                team_bill[team["name"]] = list

        con.commit()
        con.close()

        return team_bill


if __name__ == "__main__":
        init()
        pprint.pprint(get_TeamBills(True))