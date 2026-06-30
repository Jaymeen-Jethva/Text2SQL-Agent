<div align="center">

# 🤖 Text2SQL AI Agent

### Turn Natural Language into SQL Queries in Seconds ⚡

<p>
  <a href="https://github.com/Jaymeen-Jethva/Text2SQL-Agent">
    <img src="https://img.shields.io/github/stars/Jaymeen-Jethva/Text2SQL-Agent?style=for-the-badge&logo=github&color=yellow">
  </a>
  <a href="https://github.com/Jaymeen-Jethva/Text2SQL-Agent/network/members">
    <img src="https://img.shields.io/github/forks/Jaymeen-Jethva/Text2SQL-Agent?style=for-the-badge&logo=github&color=blue">
  </a>
  <a href="https://github.com/Jaymeen-Jethva/Text2SQL-Agent/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Jaymeen-Jethva/Text2SQL-Agent?style=for-the-badge&color=green">
  </a>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge">
  <img src="https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge">
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
</p>

### 🚀 Live Demo

**👉 https://huggingface.co/spaces/jaymeen1405/text2sql-ai-agent**

---

Transform natural language questions into **production-ready SQL queries** using Large Language Models with an intuitive Streamlit interface.

</div>

---

# ✨ Features

- 💬 **Natural Language → SQL:** Instantly generate queries.
- 🧠 **LLM-powered:** Uses local LLMs (Qwen2.5) via Ollama or Hugging Face.
- 📊 **Interactive Charts:** Automatically renders Plotly charts from your SQL results.
- ⚡ **Fast & Secure:** Executes read-only queries with a built-in safety engine.
- 🔍 **Schema & Semantic Aware:** Deeply profiles your data to generate a RAG-powered Semantic Layer.
- 🛡️ **Self-Healing SQL:** Automatically retries and fixes syntax errors before you even see them.
- 🔄 **Conversation Memory:** Remembers context for follow-up questions.
- ☁️ **Cloud Ready:** One-click deployment for Hugging Face Spaces.

---

# 🏗️ Architecture

```text
          User
            │
            ▼
     Streamlit UI
            │
            ▼
    Semantic Layer Generation (FAISS Vector Store)
            │
            ▼
    Prompt Engineering (Context, DDL, Schema)
            │
            ▼
     LLM (Ollama/HuggingFace)
            │
            ▼
      SQL Generation
            │
            ▼
      Secure Query Execution
            │
            ▼
   Results + Plotly Charts + Natural Language Summary
```

- **UI Layer**: Streamlit app (`app.py`)
- **Pipeline Layer**: Orchestrates ingestion and queries (`pipeline/`)
- **Services Layer**: Single responsibility services (`service/`)
- **Models Layer**: Typed Pydantic models (`models/`)
- **Storage Layer**: SQLite and FAISS (`database/`)

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Frontend | Streamlit |
| LLM | Ollama / Hugging Face Serverless API |
| Embeddings | BAAI/bge-m3 via SentenceTransformers |
| Vector Store | FAISS |
| Framework | LangChain |
| Deployment | Hugging Face Spaces / Docker |

---

# ⚙️ Installation & Deployment

Clone the repository:
```bash
git clone https://github.com/Jaymeen-Jethva/Text2SQL-Agent.git
cd Text2SQL-Agent
```

### Option 1: Standard Local Setup
Ensure Python 3.12+ is installed.
```bash
pip install -r requirements.txt
```

Since this application uses a local LLM to generate SQL securely, you need to install Ollama:
1. Download the Windows/Mac installer from the [Official Ollama Website](https://ollama.com/download).
2. Open a new terminal and download the default model (`qwen2.5:7b`):
   ```bash
   ollama run qwen2.5:7b
   ```
*(The embedding model, `BAAI/bge-m3`, will be downloaded automatically the first time you run the app!)*

Start the application:
```bash
streamlit run app.py
```

### Option 2: Docker Installation (Recommended)
If you have Docker installed, you can run the entire project (including the Streamlit UI, the Ollama server, and automatic model downloading) using a single command:
```bash
docker-compose up --build
```
Once it's ready, open your browser and go to `http://localhost:8501`.

### Option 3: Deploy on Hugging Face Spaces
This project is configured to deploy instantly on Hugging Face Spaces Free Tier.
- Simply upload the repo to a Docker Space.
- Add your `HF_TOKEN` as a repository Secret.
- Set `LLM_PROVIDER=huggingface` in Secrets to use the Serverless API!

---

# ⚙️ Configuration
All configuration is handled in `config.py` and can be overridden by a `.env` file (see `.env.example`).
- `LLM_PROVIDER`: Choose `ollama` or `huggingface`.
- `OLLAMA_BASE_URL`: URL to your Ollama instance (default: `http://localhost:11434`).
- `DEFAULT_MODEL`: Default local LLM model (default: `qwen2.5:7b`).
- `HF_TOKEN`: Your Hugging Face access token for the serverless API.
- `EMBEDDING_MODEL`: HuggingFace embedding model (default: `BAAI/bge-m3`).

---

# 🌟 Roadmap

- [x] SQLite Database Connection & Automated DDL Extraction
- [x] RAG Integration (FAISS Semantic Layer)
- [x] Secure SQL Execution Engine
- [x] Automated Chart Generation (Plotly)
- [x] Natural Language Query Explanations
- [x] Docker & Hugging Face Cloud Deployment
- [ ] Advanced Query Optimization
- [ ] Multi-Database Support (Postgres, MySQL, Snowflake)
- [ ] Export Results to CSV/Excel

---

# 🤝 Contributing

Contributions are always welcome.

1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/amazing-feature
```
3. Commit
```bash
git commit -m "Added amazing feature"
```
4. Push
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
It really helps and motivates further development!

---

[GitHub Profile](https://github.com/Jaymeen-Jethva)

</div>