# 🧠 Natural Language to SQL (NL2SQL) for Banking Data

This project showcases a small-scale AI application that uses an open-source Ollama model (e.g., Mistral) to convert natural language queries into SQL. It's designed for internal use within a banking environment, empowering business users with the ability to query data without needing technical SQL knowledge.

---

## 📦 Features

* **🔍 Convert natural language to SQL queries** using an LLM (Ollama + Mistral).
* **🧾 Query a complex mock banking database** (SQLite).
* **🧠 Metadata-aware**: The system validates table and column usage against the database schema.
* **🧑‍💼 Business-friendly**: No SQL knowledge is required for users.
* **🧮 Streamlit UI** for easy prompt input and query display.

---

## 🚀 Setup Instructions

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Generate the SQLite database with mock data:**
    ```bash
    python db_setup.py
    ```

3.  **Install and run the LLM:**
    * Download Ollama: [https://ollama.com/download](https://ollama.com/download)
    * Start the qwen3:1.7b model:
        ```bash
        ollama run qwen3:1.7b
        ```

4.  **Launch the UI:**
    ```bash
    streamlit run app.py
    ```

---

## 🧪 Sample Questions and SQL Patterns

| Question                                                          | Expected SQL                                                                       | Notes                                            |
| :---------------------------------------------------------------- | :--------------------------------------------------------------------------------- | :----------------------------------------------- |
| "Which customers have more than 3 credit cards?"                  | (Uses `GROUP BY`, `HAVING`)                                                        | Multi-row join                                   |
| "List all approved loans over $20,000 applied in Q1 2024"         | `WHERE amount > 20000 AND application_date BETWEEN '2024-01-01' AND '2024-03-31'` | Filtered time window                             |
| "Show average transaction amount per account type"                | `JOIN accounts` → `GROUP BY account_type`                                          | Aggregate by type                                |
| "Which accounts triggered high severity fraud alerts?"            | Join + `Filter by severity = 'high'`                                               | Correlation                                      |
| "Total payments received by credit card type"                     | `Join payments + credit_cards` → `GROUP BY card_type`                              | 2-table join                                     |

---

## 🗃 Database Schema (Auto-generated)

* `customers`
* `accounts`
* `transactions`
* `loan_applications`
* `credit_cards`
* `payments`
* `fraud_alerts`

Each table's structure is described in `metadata.json` for LLM-aware validation.

---

## 🤖 Model Info

* **LLM**: Mistral
* **Serving via**: Ollama
* **Prompts include**: Schema metadata and contextual information.

---