## 📊 Expense Tracker (Budget Manager)

A command-line Python application that helps users track their daily expenses, manage monthly budgets, and receive email alerts when they're close to or exceed their spending limits.

### 🔧 Features

- 💸 **Add and categorize expenses**
- 📊 **Track expenses by category and month**
- 📁 **Stores data in both CSV and SQLite database**
- 📬 **Sends email alerts when budgets are low or exceeded**
- 🔐 **Secure user-specific budget tracking**
- 📅 **Customizable budgets per month and category**
- 🧠 Uses `SQLAlchemy`, `yagmail`, and `smtplib` for storage and email handling

---

### 📁 Project Structure

```
├── expense_tracker.py      # Main script to run the app
├── expense.py              # Contains Expense and SavingsGoal classes
├── expenses.csv            # Stores logged expenses
├── budgets.csv             # Stores monthly budgets
├── expenses.db             # SQLite DB for persistent storage
```

---

### 🚀 How to Run

1. **Install Dependencies**

```bash
pip install yagmail sqlalchemy
```

> For email alerts to work, you must enable [App Passwords](https://support.google.com/accounts/answer/185833) or set up Gmail API OAuth2.

2. **Run the App**

```bash
python expense_tracker.py
```

Follow the interactive prompts to log expenses, set monthly budgets, and receive insights.

---

### 📬 Email Alerts

When you exceed a budget or approach the limit (within 10%), the app sends you an automated email notification. Make sure to:

- Replace the sender email and app password in `send_email_alert()` in `expense_tracker.py`.
- Use Gmail App Passwords or OAuth2 (for enhanced security).

---

### 💡 Future Improvements

- Add a GUI interface with `Tkinter` or `PyQt`
- Monthly expense visualizations (charts)
- Export reports to PDF or Excel
- Multi-user authentication system
