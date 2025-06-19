### pip install -r requirements.txt

### python db_setup.py

### ollama dopwnload - https://ollama.com/download
### ollama run mistral

### 🧪 Sample Questions and SQL Patterns

| Question                                                   | Expected SQL                                                                      | Notes                |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------- | -------------------- |
| "Which customers have more than 3 credit cards?"           | Uses `GROUP BY`, `HAVING`                                                         | Multi-row join       |
| "List all approved loans over $20,000 applied in Q1 2024"  | `WHERE amount > 20000 AND application_date BETWEEN '2024-01-01' AND '2024-03-31'` | Filtered time window |
| "Show average transaction amount per account type"         | `JOIN accounts → GROUP BY account_type`                                           | Aggregate by type    |
| "Which accounts triggered high severity fraud alerts?"     | Join + Filter by `severity = 'high'`                                              | Correlation          |
| "Total payments received by credit card type"              | Join `payments` + `credit_cards` → `GROUP BY card_type`                           | 2-table join         |
