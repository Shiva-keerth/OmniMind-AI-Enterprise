---
title: OmniMind AI
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: streamlit
app_file: frontend/app.py
pinned: false
---
# 🧠 OmniMind AI - Enterprise Knowledge Engine

**Live Enterprise Demo:** [OmniMind AI on Hugging Face](https://huggingface.co/spaces/farracer/OmniMind-AI-Enterprise)

## 📸 Application Interface

*(Save your UI screenshot as `dashboard.png` in an `assets` folder!)*
![OmniMind AI Dashboard](assets/dashboard.png)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph_Database-018bff.svg)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E.svg)
![LangChain](https://img.shields.io/badge/LangChain-AI_Orchestration-1c3c3c.svg)

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

## 💻 Local Development Setup

1. **Clone the repository and create a virtual environment:**
   ```bash
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
