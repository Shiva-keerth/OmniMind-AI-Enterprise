import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class GraphIngestor:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        # We initialize the Neo4j driver
        self.driver = GraphDatabase.driver(uri, auth=(user, password), database='0be7552c')

    def close(self):
        self.driver.close()

    def ingest_meeting_intelligence(self, intelligence: dict):
        """
        Takes the extracted MeetingIntelligence dictionary and MERGES it into the Neo4j Graph.
        """
        project_name = intelligence.get("project_name")
        employees = intelligence.get("employees_mentioned", [])
        action_items = intelligence.get("action_items", [])
        
        with self.driver.session() as session:
            # 1. MERGE the Project Node
            if project_name:
                session.execute_write(self._merge_project, project_name)
            
            # 2. MERGE Employee Nodes and connect them to the Project (MENTIONED_IN)
            for emp in employees:
                if emp and project_name:
                    session.execute_write(self._merge_employee_and_project, emp, project_name)
            
            # 3. MERGE Action Items, connect to Project (BELONGS_TO) and Employee (ASSIGNED_TO)
            for item in action_items:
                task = item.get("task_description")
                assignee = item.get("assignee")
                deadline = item.get("deadline")
                
                if task and project_name:
                    session.execute_write(self._merge_action_item, task, assignee, deadline, project_name)

    @staticmethod
    def _merge_project(tx, project_name):
        query = """
        MERGE (p:Project {name: $project_name})
        """
        tx.run(query, project_name=project_name)

    @staticmethod
    def _merge_employee_and_project(tx, employee_name, project_name):
        query = """
        MERGE (e:Employee {name: $employee_name})
        MERGE (p:Project {name: $project_name})
        MERGE (e)-[:MENTIONED_IN]->(p)
        """
        tx.run(query, employee_name=employee_name, project_name=project_name)

    @staticmethod
    def _merge_action_item(tx, task, assignee, deadline, project_name):
        # Create/Merge the Action Item
        # Connect it to the Project
        query_item = """
        MERGE (a:ActionItem {task: $task})
        ON CREATE SET a.deadline = $deadline
        ON MATCH SET a.deadline = $deadline
        MERGE (p:Project {name: $project_name})
        MERGE (a)-[:BELONGS_TO]->(p)
        """
        tx.run(query_item, task=task, deadline=deadline, project_name=project_name)
        
        # If there is a specific assignee, connect them!
        if assignee and assignee.lower() != "unassigned":
            query_assignee = """
            MERGE (e:Employee {name: $assignee})
            MERGE (a:ActionItem {task: $task})
            MERGE (e)-[:ASSIGNED_TO]->(a)
            """
            tx.run(query_assignee, assignee=assignee, task=task)

    def get_stats(self):
        """Returns counts of core entities in the Neo4j graph."""
        query = """
        MATCH (p:Project) WITH count(p) as projects
        MATCH (e:Employee) WITH projects, count(e) as employees
        MATCH (a:ActionItem) RETURN projects, employees, count(a) as action_items
        """
        with self.driver.session() as session:
            result = session.run(query).single()
            if result:
                return {
                    "projects": result["projects"],
                    "employees": result["employees"],
                    "action_items": result["action_items"]
                }
            return {"projects": 0, "employees": 0, "action_items": 0}

    def get_graph_data(self, limit=100):
        """Returns nodes and edges for visualizing in streamlit-agraph."""
        query = """
        MATCH (n)-[r]->(m)
        RETURN id(n) as source_id, labels(n)[0] as source_label, n.name as source_name, n.task as source_task,
               type(r) as edge_type,
               id(m) as target_id, labels(m)[0] as target_label, m.name as target_name, m.task as target_task
        LIMIT $limit
        """
        nodes = {}
        edges = []
        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            for record in result:
                s_id = record["source_id"]
                t_id = record["target_id"]
                
                if s_id not in nodes:
                    nodes[s_id] = {
                        "id": s_id, 
                        "label": record["source_label"], 
                        "title": record["source_name"] or record["source_task"] or str(s_id)
                    }
                if t_id not in nodes:
                    nodes[t_id] = {
                        "id": t_id, 
                        "label": record["target_label"], 
                        "title": record["target_name"] or record["target_task"] or str(t_id)
                    }
                
                edges.append({
                    "source": s_id,
                    "target": t_id,
                    "label": record["edge_type"]
                })
                
        return {"nodes": list(nodes.values()), "edges": edges}
