import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy .orm import sessionmaker

# load the .env file
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")

# CREATE THE ENGINE
engine = create_engine(SUPABASE_URL)

# CREATE A SESSIONMAKER
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates the tables in Supabase if they don't exist."""
    from .models import Base
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL Tables Synced Successfully!")

def save_transcript(project_name: str, raw_text: str):
    """Saves the raw meeting transcript to Supabase PostgreSQL."""
    from .models import MeetingRecord
    session = SessionLocal()
    try:
        record = MeetingRecord(project_name=project_name, raw_transcript=raw_text)
        session.add(record)
        session.commit()
        print(f"Transcript for '{project_name}' saved to Supabase!")
    except Exception as e:
        session.rollback()
        print(f"Failed to save to Supabase: {e}")
    finally:
        session.close()
