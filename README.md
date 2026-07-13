# 🧠 OmniMind AI - Enterprise Knowledge Engine

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_DB-018bff?style=for-the-badge&logo=neo4j&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![GraphRAG](https://img.shields.io/badge/Graph--RAG-Architecture-8A2BE2?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LPU_Inference-F55036?style=for-the-badge&logo=groq&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **🔗 Live Demo:** [OmniMind AI on Hugging Face](https://huggingface.co/spaces/farracer/OmniMind-AI-Enterprise) &nbsp;|&nbsp; **📂 Repository:** [GitHub](https://github.com/Shiva-keerth/OmniMind-AI-Enterprise)

---

## ✨ Highlights

- 🏢 **Enterprise Knowledge Graph** — Converts raw corporate data into structured, queryable graph intelligence
- 🧬 **Graph-RAG** — Natural language → Cypher queries via `GraphCypherQAChain`, not traditional vector-only RAG
- 🎙️ **Multi-Modal Ingestion** — Accepts raw text, PDFs, and audio (Zoom recordings) via Groq Whisper
- 📊 **Live Neo4j Visualization** — Real-time entity counts, relationship maps, and graph health metrics
- 🤖 **Agentic Extraction** — Llama-3.3-70B extracts `Projects`, `Employees`, `Action Items`, `Deadlines` automatically
- 🚀 **Production Deployment** — Live on Hugging Face Spaces with Supabase + Neo4j Aura backends

---

## 📸 Application Interface

### Global Command Center — Live Neo4j Metrics
![OmniMind AI Dashboard](assets/dashboard.png)

### Graph-RAG Corporate Knowledge Chatbot
![Graph-RAG Chat](assets/graph_rag_chat.png)

### Interactive Knowledge Graph Visualizer
![Graph Visualizer](assets/graph_visualizer.png)

---

OmniMind AI is a highly advanced, multi-modal **Enterprise Knowledge Engine** and **Graph-RAG System**. It solves the multi-billion dollar corporate problem of "Information Silos" by ingesting messy internal data (Zoom meeting audio, strategy PDFs, text documents), extracting structured actionable intelligence, and indexing it into a Knowledge Graph for natural language querying.

## 🚀 Features

- **Multi-Modal Data Ingestion:** Supports raw text, PDF parsing, and direct Audio ingestion (MP3/WAV) using Groq's lightning-fast **Whisper** model.
- **Agentic Extraction:** Utilizes **Llama-3.3-70B** via LangChain Pydantic structured outputs to extract `Projects`, `Employees`, `Action Items`, and `Key Strategic Decisions`.
- **Polyglot Persistence Architecture:**
  - **Supabase (PostgreSQL):** Stores the massive, raw meeting transcripts and documents for long-term audit compliance.
  - **Neo4j Aura (Graph DB):** Stores the complex, highly-connected relationships (`Employee -[ASSIGNED_TO]-> ActionItem -[BELONGS_TO]-> Project`).
- **Graph-RAG Chatbot:** A fully interactive HR/Management Chatbot built with `GraphCypherQAChain` that translates English questions into Cypher queries on the fly.
- **Enterprise UI:** A stunning, dark-mode Streamlit dashboard with animated sidebars and glassmorphism styling.

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Frontend
        UI[Streamlit Dashboard]
        Chat[Graph-RAG Chatbot]
    end

    subgraph Backend APIs [FastAPI]
        API_Text[/api/extract/text/]
        API_Audio[/api/extract/audio/]
        API_Chat[/api/chat/]
    end

    subgraph AI Extraction Engine [LangChain + Groq]
        Whisper[Groq Whisper Model]
        Llama3[Llama-3.3-70B Model]
        Parser[Pydantic Structured Output]
    end

    subgraph Polyglot Persistence Layer
        Neo4j[(Neo4j Graph DB)]
        Supabase[(Supabase PostgreSQL)]
    end

    %% Workflows
    UI -- "Uploads Audio (.mp3)" --> API_Audio
    UI -- "Pastes Text" --> API_Text
    Chat -- "Natural Language Q's" --> API_Chat

    API_Audio -- "Raw Audio" --> Whisper
    Whisper -- "Transcription" --> Llama3
    API_Text -- "Raw Text" --> Llama3

    Llama3 -- "Extracts Entities" --> Parser
    Parser -- "Structured JSON" --> Neo4j
    Parser -- "Raw Transcripts" --> Supabase

    API_Chat -- "Query" --> Llama3
    Llama3 -- "Generates Cypher" --> Neo4j
    Neo4j -- "Graph Results" --> Chat
```

## 🛠️ Tech Stack
* **Backend:** FastAPI, Python, Uvicorn, SQLAlchemy
* **Frontend:** Streamlit, Streamlit-Option-Menu
* **AI/ML:** LangChain, Groq API (Llama-3.3-70b-versatile, Whisper-large-v3)
* **Databases:** Neo4j (Aura Cloud), Supabase (PostgreSQL)

## ☁️ Deployment

| Layer | Platform | Details |
|-------|----------|---------|
| **Frontend** | Hugging Face Spaces | Streamlit app with custom CSS, auto-deployed |
| **Backend** | Render | FastAPI server with Uvicorn, auto-restart on push |
| **Graph Database** | Neo4j Aura (Cloud) | Managed graph instance with Bolt protocol |
| **Relational Database** | Supabase (PostgreSQL) | Managed Postgres for transcript storage & audit logs |
| **LLM Inference** | Groq Cloud | Llama-3.3-70B + Whisper-large-v3 via ultra-low-latency LPU |

## 💻 Local Development Setup

1. **Clone the repository and create a virtual environment:**
   ```bash
   git clone https://github.com/Shiva-keerth/OmniMind-AI-Enterprise.git
   cd OmniMind-AI-Enterprise
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r frontend/requirements.txt
   ```
3. **Set up Environment Variables (`.env`):**
   ```env
   GROQ_API_KEY="your-groq-key"
   SUPABASE_URL="postgresql://user:pass@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
   NEO4J_URI="neo4j+ssc://your-uri.databases.neo4j.io"
   NEO4J_USERNAME="neo4j"
   NEO4J_PASSWORD="your-neo4j-password"
   ```
4. **Run the Backend (FastAPI):**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
5. **Run the Frontend (Streamlit) in a new terminal:**
   ```bash
   streamlit run frontend/app.py
   ```
