import requests
import sqlite3
import json
from utils import load_metadata, validate_question

metadata = load_metadata()

def build_prompt(user_question):
    return f"""
You are a SQL generator. Based on the metadata below, generate SQL queries for questions strictly related to the data.

Metadata:
{json.dumps(metadata, indent=2)}

User Question:
{user_question}

If the question is unrelated to any of the metadata tables or columns, respond:
"This question is outside the scope of the available data."

Only return SQL and no explaination if the question is valid.
- Always use table.column_name to avoid ambiguity.
"""

def query_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json().get("response", "[No response from model]")
    except requests.exceptions.RequestException as e:
        return f"[LLM request error] {str(e)}"
    except ValueError:
        return "[LLM response was not valid JSON]"


def run_sql(sql_query):
    conn = sqlite3.connect("data/test.db")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results