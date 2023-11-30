import sqlite3


sqliteConnection = sqlite3.connect('instance/watching-history.db')

sql_query = """SELECT * FROM watching_history;"""

cursor = sqliteConnection.cursor()

cursor.execute(sql_query)

print(cursor.fetchall())