import sqlite3
import re
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
                profiles.append(self._profile_table(conn, table))
        return profiles

    def _get_tables(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)
        return [row[0] for row in cursor.fetchall()]

    def _profile_table(self, conn, table_name):
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        row_count = cursor.fetchone()[0]

        cursor.execute(f"PRAGMA table_info([{table_name}])")
        schema = cursor.fetchall()
        columns = []

        for column in schema:
            cid, name, sqlite_type, notnull, default_value, pk = column
            stats = self._column_statistics(conn, table_name, name, row_count, sqlite_type)
            
            profile = ColumnProfile(
                column_name=name,
                sqlite_type=sqlite_type,
                semantic_type=stats["semantic_type"],
                nullable=not bool(notnull),
                primary_key=bool(pk),
                distinct_count=stats["distinct_count"],
                null_count=stats["null_count"],
                min_value=stats["min_value"],
                max_value=stats["max_value"],
                average_value=stats.get("average_value"),
                median_value=stats.get("median_value"),
                unique_values=stats.get("unique_values", []),
                sample_values=stats.get("sample_values", []),
                is_categorical=stats.get("is_categorical", False),
                is_boolean=stats.get("is_boolean", False),
                is_currency=stats.get("is_currency", False),
                is_percentage=stats.get("is_percentage", False),
                is_date=stats.get("is_date", False),
                is_email=stats.get("is_email", False),
                is_phone=stats.get("is_phone", False),
                is_identifier=stats.get("is_identifier", False)
            )
            columns.append(profile)

        return TableProfile(
            table_name=table_name,
            row_count=row_count,
            columns=columns,
        )

    def _column_statistics(self, conn, table_name, column_name, row_count, sqlite_type):
        cursor = conn.cursor()
        
        # Get all non-null values for detailed stats
        cursor.execute(f"SELECT [{column_name}] FROM [{table_name}] WHERE [{column_name}] IS NOT NULL")
        raw_values = [r[0] for r in cursor.fetchall()]
        
        null_count = row_count - len(raw_values)
        distinct_vals = list(set(raw_values))
        distinct_count = len(distinct_vals)
        
        min_value = min(raw_values) if raw_values else None
        max_value = max(raw_values) if raw_values else None
        
        average_value = None
        median_value = None
        numeric_values = [v for v in raw_values if isinstance(v, (int, float))]
        if numeric_values:
            average_value = sum(numeric_values) / len(numeric_values)
            sorted_vals = sorted(numeric_values)
            mid = len(sorted_vals) // 2
            median_value = sorted_vals[mid]

        unique_values = distinct_vals[:20] if distinct_count <= 20 else []
        sample_values = raw_values[:5]

        # Semantic Detections
        name_lower = column_name.lower()
        
        is_identifier = name_lower.endswith("_id") or name_lower == "id" or "uuid" in name_lower
        
        is_boolean = False
        if distinct_count <= 2 and all(str(v).lower() in ["0", "1", "true", "false", "yes", "no", "y", "n"] for v in distinct_vals):
            is_boolean = True

        is_categorical = False
        if 1 < distinct_count <= 15 and row_count > 20 and not is_boolean and not is_identifier:
            is_categorical = True

        is_currency = False
        if any(kw in name_lower for kw in ["price", "amount", "cost", "revenue", "salary", "budget", "total"]):
            is_currency = True
        elif any(isinstance(v, str) and re.search(r"[$€£₹¥]", v) for v in distinct_vals[:10]):
            is_currency = True

        is_percentage = False
        if "pct" in name_lower or "percentage" in name_lower or "rate" in name_lower:
            is_percentage = True
        elif any(isinstance(v, str) and "%" in v for v in distinct_vals[:10]):
            is_percentage = True

        is_date = False
        if any(kw in name_lower for kw in ["date", "time", "created", "updated", "deleted", "at"]):
            is_date = True
        elif any(isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}", v) for v in distinct_vals[:10]):
            is_date = True

        is_email = False
        if "email" in name_lower:
            is_email = True
        elif any(isinstance(v, str) and "@" in v and "." in v for v in distinct_vals[:10]):
            is_email = True

        is_phone = False
        if "phone" in name_lower or "mobile" in name_lower or "fax" in name_lower:
            is_phone = True

        # Resolve primary semantic type
        if is_identifier: semantic_type = "IDENTIFIER"
        elif is_boolean: semantic_type = "BOOLEAN"
        elif is_date: semantic_type = "DATE"
        elif is_email: semantic_type = "EMAIL"
        elif is_phone: semantic_type = "PHONE"
        elif is_currency: semantic_type = "CURRENCY"
        elif is_percentage: semantic_type = "PERCENTAGE"
        elif is_categorical: semantic_type = "CATEGORICAL"
        else:
            sqlite_type_upper = sqlite_type.upper()
            if "INT" in sqlite_type_upper: semantic_type = "INTEGER"
            elif "REAL" in sqlite_type_upper or "FLOAT" in sqlite_type_upper: semantic_type = "FLOAT"
            else: semantic_type = "TEXT"

        return {
            "distinct_count": distinct_count,
            "null_count": null_count,
            "min_value": min_value,
            "max_value": max_value,
            "average_value": average_value,
            "median_value": median_value,
            "unique_values": unique_values,
            "sample_values": sample_values,
            "is_categorical": is_categorical,
            "is_boolean": is_boolean,
            "is_currency": is_currency,
            "is_percentage": is_percentage,
            "is_date": is_date,
            "is_email": is_email,
            "is_phone": is_phone,
            "is_identifier": is_identifier,
            "semantic_type": semantic_type
        }