from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class MeetingRecord(Base):
    __tablename__ = "meeting_records"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    raw_transcript = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
