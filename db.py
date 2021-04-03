import  os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the Task app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        self.conn = sqlite3.connect('venmo.db', check_same_thread=False)
        self.create_task_table()

    def create_task_table(self):
        try:
            self.conn.execute(
                """
                CREATE TABLE venmo(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance INTEGER
                );

            """
            )
            self.conn.commit()
        except Exception as e:
            print(e)

    def get_all_users(self):
        cursor = self.conn.execute(
            """
            SELECT * FROM venmo;
        """
        )
        venmos = []
        for row in cursor:
            venmos.append(
                {
                    "id" : row[0],
                    "name" : row[1],
                    "username" : row[2] 
                }
            )
        return venmos

    def insert_venmo_user(self, name, username, balance=0):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO venmo (name, username, balance) VALUES (?, ?, ?);
        """,
            (name, username, balance)
        )
        self.conn.commit()
        return cur.lastrowid

    def get_user_by_id(self, id):
        cur = self.conn.execute(
            """
            SELECT * FROM venmo WHERE id = ?;
        """,
        (id,)
        )
        for row in cur:
            return{
                "id" : row[0],
                "name" : row[1],
                "username" : row[2],
                "balance" : row[3]
            }
        return None
    
    def delete_user_by_id(self, id):
        self.conn.execute(
            """
            DELETE FROM venmo WHERE id = ?;    
        """,
        (id,)
        )
        self.conn.commit()

    def update(self, id, total_amount):
        self.conn.execute(
            """
            UPDATE venmo SET balance = ? WHERE id = ?;
        """,
            (total_amount, id)
        )
        self.conn.commit()

DatabaseDriver = singleton(DatabaseDriver)
