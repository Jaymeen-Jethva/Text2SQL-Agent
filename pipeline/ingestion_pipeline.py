from pathlib import Path

from service.upload_service import save_uploaded_file
from service.dataframe_service import load_dataset
from service.sqlite_service import SQLiteService
from service.ddl_service import DDLService
from service.profiler_service import ProfilerService


def run_pipeline(uploaded_file):
    """
    Complete ingestion pipeline.

    Upload
        ↓
    Save File
        ↓
    Load Dataset
        ↓
    SQLite Database
        ↓
    DDL Extraction
        ↓
    Database Profiling
    """

    # ---------------------------------------
    # Save uploaded file
    # ---------------------------------------

    local_path = save_uploaded_file(uploaded_file)

    # ---------------------------------------
    # Load dataset
    # ---------------------------------------

    dataset = load_dataset(local_path)

    # ---------------------------------------
    # SQLite
    # ---------------------------------------

    db_name = Path(uploaded_file.name).stem

    sqlite_service = SQLiteService(db_name=db_name)

    db_path = sqlite_service.dataframe_to_sqlite(
        dataset["tables"]
    )

    # ---------------------------------------
    # Extract DDL
    # ---------------------------------------

    ddl_service = DDLService(db_path)

    ddl = ddl_service.get_all_ddl()

    # ---------------------------------------
    # Profile Database
    # ---------------------------------------

    profiler = ProfilerService(db_path)

    profiles = profiler.profile_database()

    # ---------------------------------------
    # Return Pipeline Result
    # ---------------------------------------

    return {
        "dataset_name": uploaded_file.name,
        "dataset": dataset,
        "tables": list(dataset["tables"].keys()),
        "db_path": db_path,
        "ddl": ddl,
        "profiles": profiles,
    }