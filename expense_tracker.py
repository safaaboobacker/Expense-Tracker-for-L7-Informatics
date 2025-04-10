# expense.py

class Expense:
    def __init__(self, name: str, amount: float, category: str, date: str, user: str):
        self.name = name
        self.amount = amount
        self.category = category
        self.date = date
        self.user = user

    def __str__(self):
        return f"{self.name} | {self.category} | ${self.amount:.2f} | {self.date} | {self.user}"


# tracker.py
from expense import Expense
import calendar
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from collections import defaultdict
from sqlalchemy import create_engine, Column, String, Float, MetaData, Table

USER_EMAIL = "safa19161saf@gmail.com"
BUDGETS_FILE = "budgets.csv"
DATABASE_URL = "sqlite:///expenses.db"

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
expenses_table = Table("expenses", metadata,
    Column("name", String),
    Column("amount", Float),
    Column("category", String),
    Column("date", String),
    Column("user", String)
)
metadata.create_all(engine)


def main():
    print(f" Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    # Get user and month info
    user = input("Enter your name: ")
    mail = input("Enter your mail ID: ")
    month = datetime.datetime.now().strftime("%Y-%m")

    # Get budget info or set new ones
    category_budgets = get_monthly_budgets(user, month)

    # Get and save expense
    expense = get_user_expense(user)
    save_expense_to_file(expense, expense_file_path)

    # Save to SQL DB
    save_expense_to_db(expense)

    # Read and summarize
    summarize_expenses(mail, expense_file_path, category_budgets, user, month)


def get_user_expense(user):
    print(f" Getting User Expense")
    expense_name = input("Enter expense name: ")
    try:
        expense_amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return get_user_expense(user)

    expense_categories = [
        " Food",
        " Transport",
        " Entertainment",
        " Home",
        " Work",
        " Fun",
        " Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        try:
            selected_index = int(input(f"Enter a category number [1-{len(expense_categories)}]: ")) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            return Expense(name=expense_name, amount=expense_amount, category=selected_category, date=date_str, user=user)
        else:
            print("Invalid category. Please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f" Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date},{expense.user}\n")


def save_expense_to_db(expense: Expense):
    with engine.connect() as conn:
        conn.execute(expenses_table.insert().values(
            name=expense.name,
            amount=expense.amount,
            category=expense.category,
            date=expense.date,
            user=expense.user
        ))


def get_monthly_budgets(user, month):
    budgets = {}
    if os.path.exists(BUDGETS_FILE):
        with open(BUDGETS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                u, m, cat, amt = line.strip().split(",")
                if u == user and m == month:
                    budgets[cat] = float(amt)

    print(f"Current Budgets for {user} - {month}: {budgets if budgets else 'None'}")
    choice = input("Do you want to update/set budgets for this month? (y/n): ")
    if choice.lower() == 'y':
        categories = [" Food", " Transport", " Entertainment", " Home", " Work", " Fun", " Misc"]
        for cat in categories:
            amt = input(f"Enter budget for {cat}: ")
            try:
                budgets[cat] = float(amt)
            except ValueError:
                budgets[cat] = 0.0

        with open(BUDGETS_FILE, "a", encoding="utf-8") as f:
            for cat, amt in budgets.items():
                f.write(f"{user},{month},{cat},{amt}\n")

    return budgets


def summarize_expenses(mail, expense_file_path, budgets, user, month):
    print(f" Summarizing Expenses for {user} in {month}")
    expenses: list[Expense] = []

    if not os.path.exists(expense_file_path):
        print("No expense records found.")
        return

    with open(expense_file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                name, amount, category, date_str, u = line.strip().split(",")
                if u == user and date_str.startswith(month):
                    expenses.append(Expense(name, float(amount), category, date_str, u))
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")

    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp.category] += exp.amount

    print("\nExpenses by Category :")
    for cat, total in category_totals.items():
        budget = budgets.get(cat, 0)
        print(f"  {cat}: ${total:.2f} / ${budget:.2f}")
        remaining = budget - total
        if remaining < 0:
            print(red(f"     Exceeded budget by ${-remaining:.2f}"))
            send_email_alert(mail, user, cat, total, budget)
        elif budget > 0 and remaining <= 0.1 * budget:
            print(yellow(f"     Only 10% of budget left!"))
            send_email_alert(mail, user, cat, total, budget, warning=True)

    total_spent = sum([x.amount for x in expenses])
    print(f"\n Total Spent This Month: ${total_spent:.2f}\n")


import yagmail

def send_email_alert(mail, user, category, spent, budget, warning=False):
    subject = f"{'[Alert] ' if not warning else '[Warning] '}Budget {'Exceeded' if not warning else 'Low'} - {category}"
    body = (
        f"Dear {user},\n\n"
        f"You have {'exceeded' if not warning else 'nearly reached'} your budget for {category}!\n"
        f"Spent: ${spent:.2f}, Budget: ${budget:.2f}\n\nRegards,\nExpense Tracker"
    )

    try:
        yag = yagmail.SMTP("safaaboobacker10@gmail.com", "cgrn ojhy ysbs hnrf")
        yag.send(to= mail, subject=subject, contents=body)
        print(" Email sent using yagmail!")
    except Exception as e:
        print(f" Failed to send email: {e}")


def green(text):
    return f"\033[92m{text}\033[0m"

def yellow(text):
    return f"\033[93m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"


if __name__ == "__main__":
    main()
