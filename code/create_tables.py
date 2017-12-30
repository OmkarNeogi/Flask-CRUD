import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS items (name TEXT, price real);"
cursor.execute(create_table_query)

cursor.execute("INSERT INTO items VALUES (?, ?)", ("test", 10.99))

connection.commit()
connection.close()