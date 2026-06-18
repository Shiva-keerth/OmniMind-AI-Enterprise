import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USERNAME')
pwd = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(user, pwd))
with driver.session() as session:
    res = session.run("MATCH (e:Employee)-[:MENTIONED_IN]->(p:Project) WHERE p.name = 'Delta Sync' RETURN e.name")
    employees = [r['e.name'] for r in res]
    print(f"Employees mentioned in Delta Sync: {employees}")
    
    # Also test ActionItem to Project relation
    res2 = session.run("MATCH (p:Project)<-[:BELONGS_TO]-(a:ActionItem) WHERE p.name = 'Delta Sync' RETURN a.task")
    items = [r['a.task'] for r in res2]
    print(f"Action items belonging to Delta Sync: {items}")
