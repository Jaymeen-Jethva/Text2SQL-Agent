from pathlib import Path
import sqlite3

DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(exist_ok=True)


class SQLiteService:

    def __init__(self, db_name: str):
        self.db_path = DATABASE_DIR / f"{db_name}.db"

    def create_database(self):

        # Remove old database if it exists
        if self.db_path.exists():
            self.db_path.unlink()

        return sqlite3.connect(self.db_path)

    def dataframe_to_sqlite(self, tables: dict):

        connection = self.create_database()

        try:

            for table_name, df in tables.items():

                df.to_sql(
                    table_name,
                    connection,
                    if_exists="replace",
                    index=False,
                )

            connection.commit()

        finally:

            connection.close()

        return self.db_path