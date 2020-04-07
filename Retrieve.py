import sqlite3

l = []


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
    except sqlite3.Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM pcapdb")

    rows = cur.fetchall()

    for row in rows:
        # print(row)
        l.append(row)
        # print("List values")
        # print(l)
    print(l)


# def select_task_by_priority(conn, priority):
#     """
#     Query tasks by priority
#     :param conn: the Connection object
#     :param priority:
#     :return:
#     """
#     cur = conn.cursor()
#     # cur.execute("SELECT * FROM pcapdb WHERE priority=?", (priority,))
#     cur.execute('select * from pcapdb')
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print(row)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def main():
    database = r'db.testdb'

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Querying DB")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
