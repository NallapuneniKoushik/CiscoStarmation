import sqlite3

con = sqlite3.connect('filter.db')
cur = con.cursor()
with con:
    cur.execute("CREATE TABLE if not exists DATA(Protocol TEXTE, key TEXTE)")


def add_data(protocol, key):
    con = sqlite3.connect('filter.db')
    cur = con.cursor()
    cur.execute('INSERT INTO DATA values((?),(?))', (str(protocol), str(key)))
    con.commit()


def read_data():
    con = sqlite3.connect('filter.db')
    cur = con.cursor()
    dat = []
    cur.execute('SELECT Protocol from DATA')
    for rows in cur.fetchall():
        dat.append(rows)
    con.close()
    return dat


def read_specific_data(data):
    con = sqlite3.connect('filter.db')
    cur = con.cursor()
    dat = []
    cur.execute(f'SELECT key from DATA where Protocol="{data}"')
    for rows in cur.fetchall():
        dat.append(rows)
    con.close()
    return dat
