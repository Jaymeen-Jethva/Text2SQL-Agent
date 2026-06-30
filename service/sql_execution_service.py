import sqlite3
import time
from pathlib import Path
from dataclasses import dataclass
import re

@dataclass
class SQLExecutionResult:
    columns: list[str]
    rows: list[tuple]
    row_count: int
    execution_time_ms: float
    error: str | None = None

class SQLExecutionService:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        
    def execute(self, sql: str) -> SQLExecutionResult:
        start_time = time.time()
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Security checks
                sql_upper = sql.upper()
                forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "PRAGMA"]
                
                # Check for whole word matches to avoid false positives in column names
                for word in forbidden:
                    if re.search(r'\b' + word + r'\b', sql_upper):
                        raise ValueError(f"Forbidden SQL keyword detected: {word}")
                        
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                row_count = len(rows)
                exec_time = (time.time() - start_time) * 1000
                
                return SQLExecutionResult(
                    columns=columns, 
                    rows=rows, 
                    row_count=row_count, 
                    execution_time_ms=exec_time
                )
                
        except Exception as e:
            exec_time = (time.time() - start_time) * 1000
            return SQLExecutionResult(
                columns=[], 
                rows=[], 
                row_count=0, 
                execution_time_ms=exec_time, 
                error=str(e)
            )
