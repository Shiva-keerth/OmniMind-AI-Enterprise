import os
import sys
from dotenv import load_dotenv
import langchain
langchain.debug = True
from backend.services.graph_rag import GraphRAGChatbot
load_dotenv()
try:
    bot = GraphRAGChatbot()
    print('Testing query: Who are all the employees currently working on Project Delta?')
    ans = bot.ask_question('Who are all the employees currently working on Project Delta?')
    print('Answer:', ans)
except Exception as e:
    import traceback
    traceback.print_exc()
