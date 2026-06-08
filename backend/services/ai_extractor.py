import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List, Optional
from groq import Groq

# Load environment variables
load_dotenv()

# Define the exact structure we want the AI to return!
class ActionItem(BaseModel):
    task_description: str = Field(description="The specific task to be done")
    assignee: str = Field(description="The name of the employee assigned to this task. 'Unassigned' if not explicitly stated.")
    deadline: Optional[str] = Field(description="The deadline for the task, if mentioned")

class MeetingIntelligence(BaseModel):
    project_name: str = Field(description="The main project or topic being discussed")
    employees_mentioned: List[str] = Field(description="A list of all employee names mentioned in the text")
    action_items: List[ActionItem] = Field(description="A list of action items or tasks assigned")
    key_decisions: List[str] = Field(description="A list of important strategic decisions made")

class OmniExtractor:
    def __init__(self):
        # 1. Option B: Llama-3.3-70b-versatile for hyper-intelligent text extraction
        self.llm = ChatGroq(
            temperature=0, 
            groq_api_key=os.getenv("GROQ_API_KEY"), 
            model_name="llama-3.3-70b-versatile"
        )
        
        # 2. Native Groq Client for Whisper Audio
        self.audio_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def extract_intelligence(self, text: str) -> dict:
        """Extracts structured JSON data from corporate meeting transcripts or project specs."""
        # Force the LLM to output ONLY the JSON structure defined in MeetingIntelligence
        structured_llm = self.llm.with_structured_output(MeetingIntelligence)
        
        prompt = f"Extract the enterprise intelligence from the following corporate meeting transcript or project document. You MUST strictly adhere to the provided schema. For the 'action_items' field, you must return a list of nested objects (containing task_description, assignee, and deadline), NOT a list of strings. If a field is missing, leave it null or empty.\n\nTEXT:\n{text}"
        
        result = structured_llm.invoke(prompt)
        # Convert the Pydantic object back to a standard Python dictionary
        if hasattr(result, "model_dump"):
            return result.model_dump()
        elif hasattr(result, "dict"):
            return result.dict()
        return result
    
    def parse_audio_to_text(self, audio_file_path: str) -> str:
        """Converts an audio file to text using Groq Whisper."""
        with open(audio_file_path, "rb") as file:
            transcription = self.audio_client.audio.transcriptions.create(
              file=(audio_file_path, file.read()),
              model="whisper-large-v3",
              response_format="json",
              language="en",
              temperature=0.0
            )
        return transcription.text
