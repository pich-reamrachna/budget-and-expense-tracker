import json
import os

DATA_FILE = 'transactions.json'
BUDGET_FILE = 'budgets.json'

def load_transactions_from_file(app):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            app.transactions = json.load(f)
    else:
        app.transactions = []

def save_transactions_to_file(app):
    with open(DATA_FILE, 'w') as f:
        json.dump(app.transactions, f, indent=4)

def load_budgets(app):
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            app.budgets = json.load(f)
    else:
        app.budgets = {}

def save_budgets(app):
    with open(BUDGET_FILE, 'w') as f:
        json.dump(app.budgets, f, indent=4)