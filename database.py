import sqlite3

async def addRequest(data):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS requests(id integer PRIMARY KEY AUTOINCREMENT, valper text, platform text, crypto text, fiat text, user_id integer, rate REAL, range_from REAL, range_to REAL)''')
    cursor.execute('''INSERT INTO requests(valper, platform, crypto, fiat, user_id, rate, range_from, range_to) VALUES(?,?,?,?,?,?,?,?)''', (data["valper"], data["platform"], data["crypto"], data["fiat"], data["user_id"], data["rate"], data["range_from"], data["range_to"]))
    connection.commit()

    cursor.close()
    connection.close()

async def getRequests(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM requests WHERE user_id = ?''', [user_id])
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

async def getAllRequests():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM requests''')
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

async def delAllRequests(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM requests WHERE user_id = ?''', (user_id,))
    connection.commit()

    cursor.close()
    connection.close()

async def updateRate(id, new_value):
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()

    connection.execute("UPDATE requests SET rate = ? WHERE id = ? ", [new_value, id])
    connection.commit()

    cur.close()
    connection.close()

async def delRequest(id):
    connection = sqlite3.connect("database.db")
    cur = connection.cursor()

    connection.execute("DELETE FROM requests WHERE id=?", (id,))
    connection.commit()

    cur.close()
    connection.close()