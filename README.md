# Text2SQL Semantic Layer Agent

A production-grade, open-source Text2SQL platform built with Streamlit, LangChain, FAISS, and Ollama (Qwen2.5).

## Architecture
- **UI Layer**: Streamlit app (`app.py`)
- **Pipeline Layer**: Orchestrates ingestion and queries (`pipeline/`)
- **Services Layer**: Single responsibility services (`service/`)
- **Models Layer**: Typed Pydantic models (`models/`)
- **Storage Layer**: SQLite and FAISS (`database/`)

## Installation
1. Clone the repository.
2. Ensure Python 3.12+ is installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install and run [Ollama](https://ollama.ai/). Pull the default model:
   ```bash
   ollama run qwen2.5:7b
   ```

## Configuration
All configuration is handled in `config.py`.
- `OLLAMA_BASE_URL`: URL to your Ollama instance.
- `DEFAULT_MODEL`: Default LLM model.
- `EMBEDDING_MODEL`: HuggingFace embedding model (default: BAAI/bge-m3).

## Usage
Start the Streamlit application:
```bash
streamlit run app.py
```
1. Upload a CSV or Excel dataset via the sidebar.
2. The pipeline will automatically create an SQLite DB, profile it, generate a Semantic Layer, chunk and embed the schema into FAISS.
3. Chat with your data in the main window! The agent generates SQL, executes it, creates charts, and streams answers.

## Tests
Run tests with:
```bash
pytest
```