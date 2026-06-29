import sqlite3
from pathlib import Path

from models.column_profile import ColumnProfile, TableProfile


class ProfilerService:

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def profile_database(self) -> list[TableProfile]:

        profiles = []

        with sqlite3.connect(self.db_path) as conn:

            tables = self._get_tables(conn)

            for table in tables:
                profiles.append(
                    self._profile_table(conn, table)
                )

        return profiles

    def _get_tables(self, conn):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
        """)

        return [row[0] for row in cursor.fetchall()]

    def _profile_table(self, conn, table_name):

        cursor = conn.cursor()

        cursor.execute(
            f"SELECT COUNT(*) FROM [{table_name}]"
        )

        row_count = cursor.fetchone()[0]

        cursor.execute(
            f"PRAGMA table_info([{table_name}])"
        )

        schema = cursor.fetchall()

        columns = []

        for column in schema:

            (
                cid,
                name,
                sqlite_type,
                notnull,
                default_value,
                pk,
            ) = column

            stats = self._column_statistics(
                conn,
                table_name,
                name,
            )

            profile = ColumnProfile(
                column_name=name,
                sqlite_type=sqlite_type,
                semantic_type=self._infer_semantic_type(
                    name,
                    sqlite_type,
                    stats["sample_values"],
                ),
                nullable=not bool(notnull),
                primary_key=bool(pk),
                distinct_count=stats["distinct_count"],
                null_count=stats["null_count"],
                min_value=stats["min_value"],
                max_value=stats["max_value"],
                sample_values=stats["sample_values"],
            )

            columns.append(profile)

        return TableProfile(
            table_name=table_name,
            row_count=row_count,
            columns=columns,
        )

    def _column_statistics(
        self,
        conn,
        table_name,
        column_name,
    ):

        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT
                COUNT(DISTINCT [{column_name}]),
                SUM(
                    CASE
                        WHEN [{column_name}] IS NULL
                        THEN 1
                        ELSE 0
                    END
                ),
                MIN([{column_name}]),
                MAX([{column_name}])
            FROM [{table_name}]
            """
        )

        distinct_count, null_count, min_value, max_value = cursor.fetchone()

        cursor.execute(
            f"""
            SELECT [{column_name}]
            FROM [{table_name}]
            WHERE [{column_name}] IS NOT NULL
            LIMIT 5
            """
        )

        sample_values = [
            row[0]
            for row in cursor.fetchall()
        ]

        return {
            "distinct_count": distinct_count,
            "null_count": null_count or 0,
            "min_value": min_value,
            "max_value": max_value,
            "sample_values": sample_values,
        }

    def _infer_semantic_type(
        self,
        column_name,
        sqlite_type,
        sample_values,
    ):

        name = column_name.lower()

        if "date" in name or "time" in name:
            return "DATE"

        if "email" in name:
            return "EMAIL"

        if "phone" in name or "mobile" in name:
            return "PHONE"

        if "country" in name:
            return "COUNTRY"

        if (
            "price" in name
            or "amount" in name
            or "gross" in name
            or "revenue" in name
            or "salary" in name
        ):
            return "CURRENCY"

        if name.startswith("is_") or name.startswith("has_"):
            return "BOOLEAN"

        if name.endswith("_id") or name == "id":
            return "IDENTIFIER"

        sqlite_type = sqlite_type.upper()

        if sqlite_type == "INTEGER":
            return "INTEGER"

        if sqlite_type == "REAL":
            return "FLOAT"

        if sqlite_type == "TEXT":
            return "TEXT"

        return "UNKNOWN"