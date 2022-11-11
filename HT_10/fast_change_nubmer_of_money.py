import sqlite3

conn = sqlite3.connect("bankomat.db")
cur = conn.cursor()

money = [(10, 5), (20, 3), (50, 2), (100, 1), (200, 5), (500, 2), (1000, 2)]
new_money = [(y, x) for x, y in money]

cur.executemany("UPDATE Balance SET number=? WHERE denomination=?",
                new_money)

conn.commit()
conn.close()