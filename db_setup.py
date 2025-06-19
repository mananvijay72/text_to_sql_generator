import os
import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

fake = Faker()
conn = sqlite3.connect("data/test.db")
cursor = conn.cursor()

# --- Create Tables ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    dob TEXT,
    income REAL,
    segment TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    account_type TEXT,
    open_date TEXT,
    balance REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    txn_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    txn_date TEXT,
    amount REAL,
    txn_type TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loan_applications (
    loan_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    branch TEXT,
    application_date TEXT,
    amount REAL,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS credit_cards (
    credit_card_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    card_type TEXT,
    credit_limit REAL,
    issued_date TEXT,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    credit_card_id INTEGER,
    payment_date TEXT,
    amount REAL,
    method TEXT,
    FOREIGN KEY (credit_card_id) REFERENCES credit_cards(credit_card_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    alert_date TEXT,
    alert_type TEXT,
    severity TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
)
""")

# --- Insert Mock Data ---
segments = ["Gold", "Silver", "Platinum"]
account_types = ["Checking", "Savings"]
txn_types = ["debit", "credit"]
loan_status = ["approved", "rejected"]
card_types = ["Visa", "Mastercard", "Amex"]
payment_methods = ["NEFT", "UPI", "cash"]
alert_types = ["suspicious_login", "high_txn_volume", "multiple_declines"]
severities = ["low", "medium", "high"]

# Customers
for i in range(1, 51):
    cursor.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", (
        i,
        fake.name(),
        fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
        round(random.uniform(30000, 150000), 2),
        random.choice(segments)
    ))

# Accounts
acc_id = 1
for cust_id in range(1, 51):
    for _ in range(random.randint(1, 3)):
        cursor.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)", (
            acc_id,
            cust_id,
            random.choice(account_types),
            fake.date_between(start_date='-5y', end_date='today').isoformat(),
            round(random.uniform(500, 50000), 2)
        ))
        acc_id += 1

# Transactions
txn_id = 1
for acc in range(1, acc_id):
    for _ in range(random.randint(5, 20)):
        cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", (
            txn_id,
            acc,
            fake.date_between(start_date='-1y', end_date='today').isoformat(),
            round(random.uniform(-2000, 5000), 2),
            random.choice(txn_types)
        ))
        txn_id += 1

# Loan Applications
loan_id = 1
for cust_id in range(1, 51):
    for _ in range(random.randint(0, 2)):
        cursor.execute("INSERT INTO loan_applications VALUES (?, ?, ?, ?, ?, ?)", (
            loan_id,
            cust_id,
            fake.city(),
            fake.date_between(start_date='-2y', end_date='today').isoformat(),
            round(random.uniform(5000, 100000), 2),
            random.choice(loan_status)
        ))
        loan_id += 1

# Credit Cards
cc_id = 1
for cust_id in range(1, 51):
    for _ in range(random.randint(0, 3)):
        cursor.execute("INSERT INTO credit_cards VALUES (?, ?, ?, ?, ?, ?)", (
            cc_id,
            cust_id,
            random.choice(card_types),
            round(random.uniform(10000, 50000), 2),
            fake.date_between(start_date='-3y', end_date='today').isoformat(),
            random.choice(["active", "blocked"])
        ))
        cc_id += 1

# Payments
payment_id = 1
for card in range(1, cc_id):
    for _ in range(random.randint(2, 10)):
        cursor.execute("INSERT INTO payments VALUES (?, ?, ?, ?, ?)", (
            payment_id,
            card,
            fake.date_between(start_date='-1y', end_date='today').isoformat(),
            round(random.uniform(500, 5000), 2),
            random.choice(payment_methods)
        ))
        payment_id += 1

# Fraud Alerts
alert_id = 1
for acc in range(1, acc_id):
    if random.random() < 0.2:
        for _ in range(random.randint(1, 3)):
            cursor.execute("INSERT INTO fraud_alerts VALUES (?, ?, ?, ?, ?)", (
                alert_id,
                acc,
                fake.date_between(start_date='-6mo', end_date='today').isoformat(),
                random.choice(alert_types),
                random.choice(severities)
            ))
            alert_id += 1

conn.commit()
conn.close()
print("✅ Database created successfully.")