import os
from langchain_groq import ChatGroq
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from dotenv import load_dotenv

load_dotenv()

from langchain.prompts import PromptTemplate

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
IMPORTANT GRAPH SCHEMA RULES:
- Project nodes have a 'name' property (NOT title).
- Employee nodes have a 'name' property.
- ActionItem nodes have 'task' and 'deadline' properties.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
IMPORTANT: Do not wrap the cypher in ```cypher code blocks. Return ONLY the raw cypher string.

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

QA_TEMPLATE = """You are an AI assistant tasked with translating database JSON into a human sentence.

Database Results:
{context}

Question:
{question}

Instructions:
1. If the Database Results contain ANY data (like a dictionary or list), you MUST use that data to answer the Question.
2. Assume the Database Results are 100% correct and belong to the person/entity asked about, even if their name is missing from the JSON.
3. Simply rephrase the JSON data into a friendly sentence.
4. ONLY if the Database Results are exactly empty `[]` or None, reply with "I couldn't find that in the database."
"""

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=QA_TEMPLATE
)

class GraphRAGChatbot:
    def __init__(self):
        # 1. Connect to Neo4j Graph
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        
        # We use LangChain's built-in Neo4j wrapper
        self.graph = Neo4jGraph(url=uri, username=user, password=password, database=user)
        
        # 2. Initialize the LLM (Llama-3) for converting English to Cypher and Cypher to English
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )
        
        # 3. Create the LangChain Graph QA Chain
        self.chain = GraphCypherQAChain.from_llm(
            cypher_llm=self.llm,
            qa_llm=self.llm,
            graph=self.graph,
            verbose=True,
            cypher_prompt=CYPHER_GENERATION_PROMPT,
            qa_prompt=QA_PROMPT,
            allow_dangerous_requests=True # Required to let LLM run cypher queries
        )

    def ask_question(self, question: str) -> str:
        """Takes a natural language question and answers it using Graph-RAG."""
        try:
            # The chain will:
            # 1. Understand the Graph Schema
            # 2. Write a Cypher query based on the question
            # 3. Execute the query
            # 4. Formulate a human-readable answer
            
            # We explicitly tell it the schema so it knows the node labels
            response = self.chain.invoke({"query": question})
            return response.get("result", "I couldn't find an answer in the graph.")
        except Exception as e:
            return f"Error executing Graph-RAG: {e}"
