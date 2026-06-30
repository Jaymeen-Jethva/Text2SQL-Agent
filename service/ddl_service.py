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

    def get_table_metadata(self, table_name: str):
        """Extract detailed metadata for a single table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            columns = cursor.fetchall()
            
            cursor.execute(f"PRAGMA foreign_key_list([{table_name}])")
            foreign_keys = cursor.fetchall()
            
            cursor.execute(f"PRAGMA index_list([{table_name}])")
            indexes = cursor.fetchall()
            
            return {
                "columns": columns,
                "foreign_keys": foreign_keys,
                "indexes": indexes
            }

    def get_database_metadata(self):
        """Extract complete database DDL metadata including views and indexes."""
        metadata = {
            "tables": {},
            "views": {},
            "indexes": {}
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, sql
                FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
            """)
            for row in cursor.fetchall():
                metadata["tables"][row[0]] = row[1]
                
            cursor.execute("""
                SELECT name, sql
                FROM sqlite_master
                WHERE type='view'
                ORDER BY name;
            """)
            for row in cursor.fetchall():
                metadata["views"][row[0]] = row[1]
                
            cursor.execute("""
                SELECT name, sql
                FROM sqlite_master
                WHERE type='index' AND sql IS NOT NULL
                ORDER BY name;
            """)
            for row in cursor.fetchall():
                metadata["indexes"][row[0]] = row[1]
                
        return metadata

    def get_all_ddl(self):
        """
        Returns full schema DDL combining tables and views.
        """
        metadata = self.get_database_metadata()
        ddl = {}
        for t, sql in metadata["tables"].items():
            ddl[t] = sql
        for v, sql in metadata["views"].items():
            ddl[v] = sql
        return ddl