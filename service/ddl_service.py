import sqlite3
from pathlib import Path


class DDLService:

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def get_table_names(self):
        """Return all user tables."""

        with sqlite3.connect(self.db_path) as conn:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
            """)

            return [row[0] for row in cursor.fetchall()]

    def get_create_statement(self, table_name: str):
        """Return CREATE TABLE statement."""

        with sqlite3.connect(self.db_path) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT sql
                FROM sqlite_master
                WHERE type='table'
                AND name = ?
                """,
                (table_name,),
            )

            row = cursor.fetchone()

            return row[0] if row else None

    def get_all_ddl(self):
        """
        Returns
        -------
        dict

        {
            "customers": "CREATE TABLE ...",
            "orders": "CREATE TABLE ..."
        }
        """

        ddl = {}

        tables = self.get_table_names()

        for table in tables:
            ddl[table] = self.get_create_statement(table)

        return ddl