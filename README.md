# 💸 Expense Tracker

A personal expense tracker with budgeting, categorization, and email alerting — built with **Python**, **Flask**, **HTML/JS**, and **SQLite**.

---

## 📦 Features

- ➕ Add and save daily expenses
- 📊 Set monthly budgets by category
- 📧 Receive email alerts when budgets are exceeded
- 🔎 Summarize expenses for a selected user and month
- 🖥️ Simple web-based frontend
- 🗃️ Data storage via CSV and SQLite
- 🌐 API support using Flask backend

---

## 🔧 Tech Stack

- Python 3
- Flask + Flask-CORS
- HTML + JavaScript
- SQLite + SQLAlchemy
- yagmail (for sending emails)

---

## 🚀 Getting Started

### 1. Clone the Repository

`git clone <your-repo-url>`

### 2. Install Dependencies

- Python packages:
  - flask
  - flask-cors
  - sqlalchemy
  - yagmail

Use `pip install` for each if needed.

### 3. Run Backend Server

`python api_server.py`

Server runs at: `http://localhost:5000`

### 4. Serve Frontend

In the root directory, run:

`python -m http.server`

Then visit: `http://localhost:8000`

---

## 🧪 How to Use

1. **Set Budgets**  
   Input your name and set budgets in JSON format (e.g., `{ "Food": 200, "Transport": 100 }`).

2. **Submit Expense**  
   Fill in expense details including name, amount, category, and date.

3. **Generate Summary**  
   Enter your name and email. Summary is printed server-side, and alerts are emailed if needed.

---

## 📁 Project Structure

- `expense.py` – Expense and SavingsGoal classes
- `expense_tracker.py` – Budget logic, expense logging, summary, email alerting
- `api_server.py` – Flask API for frontend communication
- `index.html` – Web-based frontend
- `expenses.csv` – Logs of all expenses
- `budgets.csv` – Logs of all budgets
- `expenses.db` – SQLite DB (optional persistent storage)

---

## 📬 Email Alerts

- Uses `yagmail` to send budget warnings and exceeded notifications.
- Make sure to configure the sender email/password inside `send_email_alert`.

---

## 🧠 Todo / Improvements

- Add login/auth system
- Display budget summary on frontend
- Add charts (e.g., pie chart of categories)
- Deploy online with Docker or cloud
