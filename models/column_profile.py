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
    min_value: Any | None = None
    max_value: Any | None = None
    average_value: Any | None = None
    median_value: Any | None = None
    unique_values: list[Any] = []
    sample_values: list[Any] = []
    
    # Detections
    is_categorical: bool = False
    is_boolean: bool = False
    is_currency: bool = False
    is_percentage: bool = False
    is_date: bool = False
    is_email: bool = False
    is_phone: bool = False
    is_identifier: bool = False


class TableProfile(BaseModel):
    table_name: str
    row_count: int
    columns: list[ColumnProfile]