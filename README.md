# Text2SQL Semantic Layer Agent

A production-grade, open-source Text2SQL platform built with Streamlit, LangChain, FAISS, and Ollama (Qwen2.5).

## Architecture
- **UI Layer**: Streamlit app (`app.py`)
- **Pipeline Layer**: Orchestrates ingestion and queries (`pipeline/`)
- **Services Layer**: Single responsibility services (`service/`)
- **Models Layer**: Typed Pydantic models (`models/`)
- **Storage Layer**: SQLite and FAISS (`database/`)

## Installation

### 1. Project Dependencies
Ensure Python 3.12+ is installed. Then install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Install Ollama & Language Model
Since this application uses a local LLM to generate SQL securely, you need to install Ollama:

**For Windows Users:**
1. Download the Windows installer from the [Official Ollama Website](https://ollama.com/download/windows).
2. Run the executable and follow the installation steps.
3. Open a new **PowerShell** or Command Prompt window.
4. Download the default model (`qwen2.5:7b`) by running:
   ```powershell
   ollama run qwen2.5:7b
   ```
   *Note: This model is a few gigabytes in size. Once it finishes downloading and provides a prompt, you can type `/bye` to exit. Ollama will remain running in your system tray.*

### 3. Embedding Model
The embedding model (`BAAI/bge-m3`) does **not** need to be downloaded manually! The `sentence-transformers` Python package will automatically download it the very first time you run the app and upload a dataset.

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