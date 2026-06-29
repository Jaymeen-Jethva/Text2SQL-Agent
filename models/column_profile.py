from typing import Any
from pydantic import BaseModel


class ColumnProfile(BaseModel):
    column_name: str
    sqlite_type: str
    semantic_type: str
    nullable: bool
    primary_key: bool
    distinct_count: int
    null_count: int
    min_value: Any | None
    max_value: Any | None
    sample_values: list[Any]


class TableProfile(BaseModel):
    table_name: str
    row_count: int
    columns: list[ColumnProfile]