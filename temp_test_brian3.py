import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
uri = os.environ['NEO4J_URI']
user = os.environ['NEO4J_USERNAME']
pwd = os.environ['NEO4J_PASSWORD']
database = os.environ.get('NEO4J_DATABASE', user)

driver = GraphDatabase.driver(uri, auth=(user, pwd))
with driver.session(database=database) as session:
    res = session.run('MATCH (e:Employee)-[:ASSIGNED_TO]->(a:ActionItem) WHERE toLower(e.name) CONTAINS toLower("brian") RETURN e.name, a.task, a.deadline')
    print('Brian tasks:', [dict(r) for r in res])
