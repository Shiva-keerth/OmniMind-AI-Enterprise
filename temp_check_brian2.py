import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USERNAME')
pwd = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(user, pwd))
with driver.session() as session:
    res = session.run("MATCH (e:Employee)-[:ASSIGNED_TO]->(a:ActionItem) WHERE e.name = 'Brian' RETURN a.task, a.deadline")
    for r in res:
        print(dict(r))
