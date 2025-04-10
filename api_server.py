from flask import Flask, request, jsonify
from expense import Expense
from expense_tracker import (
    save_expense_to_file,
    save_expense_to_db,
    get_monthly_budgets,
    summarize_expenses,
)
import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/api/set-budgets', methods=['POST'])
def set_budgets():
    data = request.json
    user = data['user']
    month = datetime.datetime.now().strftime("%Y-%m")
    budgets = data['budgets']
    
    # Save to CSV manually
    with open("budgets.csv", "a", encoding="utf-8") as f:
        for cat, amt in budgets.items():
            f.write(f"{user},{month},{cat},{amt}\n")

    return jsonify({"message": "Budgets updated successfully!"})


@app.route('/api/submit-expense', methods=['POST'])
def submit_expense():
    data = request.json
    expense = Expense(
        name=data["name"],
        amount=data["amount"],
        category=data["category"],
        date=data["date"],
        user=data["user"]
    )

    save_expense_to_file(expense, "expenses.csv")
    save_expense_to_db(expense)

    return jsonify({"message": "Expense submitted successfully!"})


@app.route('/api/summary', methods=['POST'])
def summary():
    data = request.json
    user = data["user"]
    mail = data["mail"]
    month = datetime.datetime.now().strftime("%Y-%m")
    budgets = get_monthly_budgets(user, month)

    # For now, just reuse summarize_expenses (it prints to console),
    # later we can refactor to return a JSON response.
    summarize_expenses(mail, "expenses.csv", budgets, user, month)
    
    return jsonify({"message": "Summary printed on server (enhanced API coming soon)"})

if __name__ == "__main__":
    app.run(debug=True)
