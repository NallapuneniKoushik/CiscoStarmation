
from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


# @app.route('/enternew')
# def new_data():
#     return render_template('index.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            hostname = request.form['hostname']
            username = request.form['username']
            password = request.form['password']
            arguments = request.form['arguments']

            with sql.connect("testdb.db") as con:
                cur = con.cursor()

                cur.execute(f"INSERT INTO students pcap_table(hostname,username,password,arguments) "
                            f"values({hostname},{username},{password},{arguments}) ")

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("index.html", msg=msg)
            con.close()


@app.route('/index')
def list():
    con = sql.connect("testdb.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from pcap_table")

    rows = cur.fetchall()
    return render_template("index.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)