from pathlib import Path

from models.pipeline_result import PipelineResult

from service.upload_service import save_uploaded_file
from service.dataframe_service import load_dataset
from service.sqlite_service import SQLiteService
from service.ddl_service import DDLService
from service.profiler_service import ProfilerService
from service.semantic_layer_service import SemanticLayerService
from service.training_doc_service import TrainingDocumentService
from service.chunking_service import ChunkingService
from service.vector_store_service import VectorStoreService
from config import UPLOAD_DIR


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
    # Semantic Layer
    # ---------------------------------------

    semantic_layer_service = SemanticLayerService(db_path, profiles)
    semantic_layer = semantic_layer_service.generate()

    # ---------------------------------------
    # Training Document
    # ---------------------------------------

    training_doc_service = TrainingDocumentService(semantic_layer, ddl)
    training_doc_path = UPLOAD_DIR / f"{db_name}_training_doc.md"
    training_doc_service.save_document(training_doc_path)

    # ---------------------------------------
    # Chunking & Embeddings
    # ---------------------------------------

    chunking_service = ChunkingService(semantic_layer, ddl, db_name)
    chunks = chunking_service.generate_chunks()

    vector_store = VectorStoreService(index_name=f"{db_name}_index")
    vector_store.update_incremental(chunks)

    # ---------------------------------------
    # Return Pipeline Result
    # ---------------------------------------

    sqlite_tables = ddl_service.get_table_names()

    return PipelineResult(
        dataset_name=uploaded_file.name,
        database_path=db_path,
        tables=dataset["tables"],
        sqlite_tables=sqlite_tables,
        ddl=ddl,
        profiles=profiles,
    )