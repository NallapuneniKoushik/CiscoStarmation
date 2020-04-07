import sqlite3
from builtins import Exception


def insert_record(values):
    """inserting the new records into database"""
    hostname = values['hostname']
    username = values['username']
    password = values['password']
    arguments = values['arguments']
    status = values['status']
    db_file_name = 'client_data.db'
    with sqlite3.connect(db_file_name) as db_connection_handle:
        try:
            db_cursor = db_connection_handle.cursor()
            db_cursor.execute(
                f"INSERT INTO PCAPDB VALUES('{hostname}','{username}','{password}','{arguments}', '{status}')")
            db_connection_handle.commit()
            msg = 'Successful'
        except Exception:
            db_connection_handle.rollback()
            msg = "Error"
        finally:
            db_cursor.close()
    return msg


def read_records():
    """reading the records from database"""
    db_file_name = 'client_data.db'
    with sqlite3.connect(db_file_name) as db_connection_handle:
        db_cursor = db_connection_handle.cursor()
        db_cursor.execute('SELECT ROWID, * FROM PCAPDB')
        data = dict()
        for row in db_cursor.fetchall():
            row_dict = dict()
            for column_name, value in zip(db_cursor.description, row):
                row_dict[column_name[0]] = value
            row_dict['slug'] = row_dict['rowid']
            data[row_dict['rowid']] = row_dict
        db_cursor.close()
        return data


def update_status(values):
    """updates status accordingly where the process is exactly present"""
    hostname = values['hostname']
    username = values['username']
    arguments = values['arguments']
    status = values['status']
    db_file_name = 'client_data.db'
    with sqlite3.connect(db_file_name) as db_connection_handle:
        try:
            db_cursor = db_connection_handle.cursor()
            db_cursor.execute(
                f"UPDATE PCAPDB SET STATUS='{status}' WHERE USERNAME='{username}' AND HOSTNAME='{hostname}'"
                f" AND ARGUMENTS='{arguments}'")
            db_connection_handle.commit()
            msg = 'Successful'
        except Exception:
            db_connection_handle.rollback()
            msg = "Error"
        finally:
            db_cursor.close()
    return msg


def delete_record_db(rowid):
    """for deleting the records from database"""
    db_file_name = 'client_data.db'
    with sqlite3.connect(db_file_name) as db_connection_handle:
        try:
            db_cursor = db_connection_handle.cursor()
            db_cursor.execute(
                f"DELETE FROM PCAPDB WHERE ROWID='{rowid}'")
            db_connection_handle.commit()
            msg = 'Successful'
        except Exception:
            db_connection_handle.rollback()
            msg = "Error"
        finally:
            db_cursor.close()
    return msg
