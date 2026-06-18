import os
from langchain_groq import ChatGroq
from langchain_core.prompts.prompt import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.environ["GROQ_API_KEY"]
)

QA_PROMPT_TEMPLATE = """You are an AI assistant tasked with translating database JSON into a human sentence.

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

qa_prompt = PromptTemplate(
    template=QA_PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

chain = qa_prompt | llm

# Test 1: With name
context_1 = "[{'e.name': 'Brian', 'a.task': 'write the security documentation'}]"
res_1 = chain.invoke({"context": context_1, "question": "What is Brian working on before Friday?"})
print("Test 1 Result:", res_1.content)

# Test 2: Without name
context_2 = "[{'a.task': 'write the security documentation'}]"
res_2 = chain.invoke({"context": context_2, "question": "What is Brian working on before Friday?"})
print("Test 2 Result:", res_2.content)

# Test 3: empty
context_3 = "[]"
res_3 = chain.invoke({"context": context_3, "question": "What is Brian working on before Friday?"})
print("Test 3 Result:", res_3.content)
