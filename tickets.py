import sqlite3

con = sqlite3.connect("tickets.db")

with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS mytickets")
	cur.execute("CREATE TABLE mytickets(ticket_id INTEGER PRIMARY KEY AUTOINCREMENT, issue TEXT NOT NULL, due_date TEXT NOT NULL, priority TEXT NOT NULL, status INTEGER NOT NULL)")
	cur.execute("INSERT INTO mytickets (issue, due_date, priority, status) VALUES ('Internet not working', '05/28/2014', 'High', 1)")
	cur.execute("INSERT INTO mytickets (issue, due_date, priority, status) VALUES ('Monitor display is blank', '05/28/2014', 'High', 0)")
con.close()	