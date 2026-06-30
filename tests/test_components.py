import pytest
import pandas as pd
from pathlib import Path
from service.sqlite_service import SQLiteService
from service.profiler_service import ProfilerService

def test_sqlite_service(tmp_path):
    df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    svc = SQLiteService("test_db")
    svc.db_path = tmp_path / "test.db"
    
    db_path = svc.dataframe_to_sqlite({"users": df})
    assert db_path.exists()

def test_profiler_service(tmp_path):
    df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    svc = SQLiteService("test_prof")
    svc.db_path = tmp_path / "test_prof.db"
    db_path = svc.dataframe_to_sqlite({"users": df})
    
    profiler = ProfilerService(db_path)
    profiles = profiler.profile_database()
    
    assert len(profiles) == 1
    assert profiles[0].table_name == "users"
    assert len(profiles[0].columns) == 2
