import sqlite3


def list_tables(db_path):

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute("""

        SELECT name

        FROM sqlite_master

        WHERE type='table' AND name NOT LIKE 'sqlite_%'

    """)

    tables = cursor.fetchall()

    connection.close()

    return [x[0] for x in tables]