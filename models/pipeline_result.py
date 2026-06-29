from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class PipelineResult:

    dataset_name: str
    database_path: Path
    tables: dict[str, pd.DataFrame]
    sqlite_tables: list[str]