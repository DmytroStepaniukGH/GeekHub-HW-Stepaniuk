import sqlite3

conn = sqlite3.connect("bankomat.db")
cur = conn.cursor()

money = [(10, 7), (20, 3), (50, 1), (100, 1), (200, 3), (500, 3), (1000, 2)]
new_money = [(y, x) for x, y in money]

cur.executemany("UPDATE Balance SET number=? WHERE denomination=?",
                new_money)

conn.commit()
conn.close()