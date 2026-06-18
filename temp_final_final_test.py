import os
import langchain
langchain.debug = True
from langchain_groq import ChatGroq
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from dotenv import load_dotenv

load_dotenv()

class GraphRAGChatbot:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.environ["GROQ_API_KEY"]
        )

        CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
IMPORTANT GRAPH SCHEMA RULES:
- Project nodes have a 'name' property (NOT title).
- Employee nodes have a 'name' property.
- ActionItem nodes have 'task' and 'deadline' properties.

CRITICAL CYPHER SYNTAX RULES:
- ALWAYS use valid Cypher arrow syntax: `(a)-[:REL]->(b)` or `(a)<-[:REL]-(b)`. NEVER use invalid syntax like `(a)-[:REL]<-(b)`.
- Use `toLower()` and `CONTAINS` for fuzzy text matching.
- NEVER introduce new variables inside a WHERE NOT pattern (e.g. use `WHERE NOT (a)<-[:ASSIGNED_TO]-()` instead of `(e:Employee)`).

EXAMPLES (USE THESE EXACT PATTERNS):
Question: "What action items is Michael assigned to?"
Cypher: MATCH (e:Employee)-[:ASSIGNED_TO]->(a:ActionItem) WHERE toLower(e.name) CONTAINS toLower("michael") RETURN e.name, a.task

Question: "What are all the action items required for Project Delta?"
Cypher: MATCH (a:ActionItem)-[:BELONGS_TO]->(p:Project) WHERE toLower(p.name) CONTAINS toLower("delta") RETURN a.task, a.deadline

Question: "Who are all the employees currently working on Project Delta?"
Cypher: MATCH (e:Employee)-[:MENTIONED_IN]->(p:Project) WHERE toLower(p.name) CONTAINS toLower("delta") RETURN e.name

Question: "What is Brian working on before Friday?"
Cypher: MATCH (e:Employee)-[:ASSIGNED_TO]->(a:ActionItem) WHERE toLower(e.name) CONTAINS toLower("brian") RETURN e.name, a.task, a.deadline

Question: "Are there any unassigned tasks in the system?"
Cypher: MATCH (a:ActionItem) WHERE NOT (a)<-[:ASSIGNED_TO]-() RETURN a.task, a.deadline

Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
IMPORTANT: Do not wrap the cypher in ```cypher code blocks. Return ONLY the raw cypher string.

The question is:
{question}"""

        from langchain_core.prompts.prompt import PromptTemplate
        self.cypher_prompt = PromptTemplate(
            template=CYPHER_GENERATION_TEMPLATE,
            input_variables=["schema", "question"]
        )

        self.graph = Neo4jGraph(
            url=os.environ["NEO4J_URI"],
            username=os.environ["NEO4J_USERNAME"],
            password=os.environ["NEO4J_PASSWORD"]
        )
        
        QA_PROMPT_TEMPLATE = """You are an AI assistant tasked with translating database JSON into a human sentence.

Database Results:
{context}

Question:
{question}

Instructions:
1. If the Database Results contain ANY data (like a dictionary or list), you MUST use that data to answer the Question.
2. Assume the Database Results are 100% correct and belong to the person/entity asked about.
3. Simply rephrase the JSON data into a friendly sentence.
4. ONLY if the Database Results are exactly empty `[]` or None, reply with "I couldn't find that in the database."
"""
        self.qa_prompt = PromptTemplate(
            template=QA_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

        self.chain = GraphCypherQAChain.from_llm(
            graph=self.graph,
            cypher_llm=self.llm,
            qa_llm=self.llm,
            cypher_prompt=self.cypher_prompt,
            qa_prompt=self.qa_prompt,
            verbose=True,
            return_direct=False
        )

    def ask_question(self, question: str) -> str:
        try:
            self.graph.refresh_schema()
            response = self.chain.invoke({"query": question})
            return response.get("result", "I couldn't find an answer.")
        except Exception as e:
            return f"Error executing Graph-RAG: {str(e)}"

if __name__ == "__main__":
    bot = GraphRAGChatbot()
    print("Test 1:")
    print(bot.ask_question("Are there any unassigned tasks in the system?"))
    print("\nTest 2:")
    print(bot.ask_question("What is Brian working on before Friday?"))
