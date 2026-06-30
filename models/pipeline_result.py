from pydantic import BaseModel, ConfigDict
from pathlib import Path
import pandas as pd

from models.column_profile import TableProfile

class PipelineResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    dataset_name: str
    database_path: Path
    tables: dict[str, pd.DataFrame]
    sqlite_tables: list[str]
    ddl: dict[str, str | None]
    profiles: list[TableProfile]