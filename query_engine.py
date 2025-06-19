import requests
import sqlite3
import json
import pandas as pd
from utils import load_metadata, validate_question

metadata = load_metadata()

def build_prompt(user_question):
    return f"""
You are a Sqlite3 SQL generator. Based on the metadata below, generate only SQL queries for questions strictly related to the data.

Metadata:
{json.dumps(metadata, indent=2)}

User Question:
{user_question}

If the question is unrelated to any of the metadata tables or columns, respond:
"This question is outside the scope of the available data."

Only return SQL and no explaination or any other text if the question is valid.
- Always use table.column_name to avoid ambiguity.
- The sql query should be valid and executable.
- Sql query will run in sqlite3 database.
"""

def query_llm(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "qwen3:1.7b.", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json().get("response", "[No response from model]")
    except requests.exceptions.RequestException as e:
        return f"[LLM request error] {str(e)}"
    except ValueError:
        return "[LLM response was not valid JSON]"


def run_sql(sql_query):
    conn = sqlite3.connect("data/test.db")  # or "data/bank_demo.db"
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df