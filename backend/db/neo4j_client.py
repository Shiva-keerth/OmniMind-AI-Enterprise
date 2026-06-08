import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# 1. Load Secrets
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# 2. Create the Connection Driver
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# 3. Test the connection
driver.verify_connectivity()
print("Neo4j Graph Database Connected Successfully!")
