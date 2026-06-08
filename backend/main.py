import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from services.ai_extractor import OmniExtractor
from services.graph_ingestor import GraphIngestor
from services.graph_rag import GraphRAGChatbot
from db.postgres_client import init_db, save_transcript
import shutil
import os

app = FastAPI(title="OmniMind AI Backend")

# Initialize our new Extractor Service
extractor = OmniExtractor()
ingestor = GraphIngestor()
rag_chatbot = GraphRAGChatbot()

# Initialize Supabase Tables
init_db()

class TextPayload(BaseModel):
    text: str

class ChatPayload(BaseModel):
    question: str

@app.get("/status")
def status():
    return {"message": "Welcome to OmniMind AI Backend!"}

@app.post("/api/extract/text")
def extract_text(payload: TextPayload):
    """Takes raw text and returns a structured MeetingIntelligence JSON."""
    intelligence = extractor.extract_intelligence(payload.text)
    
    # Save to Neo4j Graph!
    try:
        ingestor.ingest_meeting_intelligence(intelligence)
    except Exception as e:
        print(f"Graph Ingestion Failed: {e}")
        
    # Save raw text to Supabase Postgres!
    try:
        project_name = intelligence.get("project_name", "Unknown Project")
        save_transcript(project_name, payload.text)
    except Exception as e:
        print(f"Supabase Ingestion Failed: {e}")
        
    return {"status": "success", "data": intelligence}

@app.post("/api/extract/audio")
async def extract_audio(file: UploadFile = File(...)):
    """Takes an audio file, transcribes it, and extracts the profile."""
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        transcription = extractor.parse_audio_to_text(temp_path)
        intelligence = extractor.extract_intelligence(transcription)
        
        # Save to Neo4j Graph!
        try:
            ingestor.ingest_meeting_intelligence(intelligence)
        except Exception as e:
            print(f"Graph Ingestion Failed: {e}")
            
        # Save raw transcription to Supabase Postgres!
        try:
            project_name = intelligence.get("project_name", "Unknown Project")
            save_transcript(project_name, transcription)
        except Exception as e:
            print(f"Supabase Ingestion Failed: {e}")
            
        return {
            "status": "success", 
            "transcription": transcription, 
            "data": intelligence
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/api/chat")
def chat_with_graph(payload: ChatPayload):
    """Takes a natural language question and answers it using Graph-RAG."""
    answer = rag_chatbot.ask_question(payload.question)
    return {"status": "success", "answer": answer}

@app.get("/api/stats")
def get_graph_stats():
    """Returns the total number of projects, employees, and action items in Neo4j."""
    try:
        stats = ingestor.get_stats()
        return {"status": "success", "data": stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/graph_data")
def get_graph_visualization_data():
    """Returns nodes and edges for the 3D graph visualizer."""
    try:
        data = ingestor.get_graph_data()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}