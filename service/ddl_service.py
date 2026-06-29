import sqlite3
from pathlib import Path

class DDLService:
    def __init__(self, db_path: Path):
        self.db_path = db_path


    def get_table_names(self):
        """Retrieve the list of table names from the SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
            return tables
        except sqlite3.Error as e:
            print(f"Error retrieving table names: {e}")
            return []


    def get_create_statement(self, table_name: str):
        with sqlite3.connect(self.db_path) as conn:
            
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT sql
                FROM sqlite_master
                WHERE type='table'
                AND name=?
                """,
                (table_name,),
            )

            row = cursor.fetchone()

            return row[0] if row else None