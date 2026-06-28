from pathlib import Path

from service.upload_service import save_uploaded_file
from service.dataframe_service import load_dataset
from service.sqlite_service import SQLiteService


def run_pipeline(uploaded_file):
    """
    Complete ingestion pipeline.

    Upload
        ↓
    Save File
        ↓
    Load Dataset
        ↓
    Convert to SQLite
    """

    # Save uploaded file
    local_path = save_uploaded_file(uploaded_file)

    # Load CSV / Excel
    dataset = load_dataset(local_path)

    # Database name = filename without extension
    db_name = Path(uploaded_file.name).stem

    # Create SQLite database
    sqlite = SQLiteService(db_name=db_name)

    db_path = sqlite.dataframe_to_sqlite(
        dataset["tables"]
    )

    return {
        "dataset": dataset,
        "db_path": db_path,
        "tables": list(dataset["tables"].keys()),
        "dataset_name": uploaded_file.name,
    }