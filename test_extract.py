import os
from backend.services.ai_extractor import OmniExtractor

def test():
    extractor = OmniExtractor()
    text = """David: Alright team, let's kick off Project Alpha. The goal here is to migrate our legacy recommendation engine to a graph-based system using Neo4j by Q4.
Sarah: I've looked at the current schema. The migration is definitely feasible, but I'll need to set up the new Neo4j cluster first. I can get that done by next Tuesday.
Alex: While Sarah is setting up the cluster, I'll start mapping the entity relationships. We need to define exactly how Users connect to Products and Categories.
David: Great. So, Sarah, your task is to provision the Neo4j cluster. Deadline is next Tuesday. Alex, you're mapping the entity relationships. Let's aim to have the first draft of the schema by Thursday."""
    try:
        res = extractor.extract_intelligence(text)
        print("SUCCESS:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
