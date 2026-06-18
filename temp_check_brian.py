import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USERNAME')
pwd = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(user, pwd))
with driver.session() as session:
    query = "MATCH (e:Employee)-[:ASSIGNED_TO]->(a:ActionItem) WHERE toLower(e.name) CONTAINS toLower('brian') AND toLower(a.deadline) CONTAINS toLower('friday') RETURN a.task"
    res = session.run(query)
    data = [dict(r) for r in res]
    print(f"Cypher query result for Brian: {data}")
