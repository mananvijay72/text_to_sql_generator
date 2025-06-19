import json

def load_metadata():
    with open("metadata.json") as f:
        return json.load(f)

def validate_question(question, metadata):
    """Basic validation if question includes table or column from metadata"""
    return any(table in question.lower() for table in metadata.keys())