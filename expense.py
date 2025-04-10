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

    def __repr__(self):
        return f"<Expense name='{self.name}' category='{self.category}' amount={self.amount:.2f} date={self.date} user={self.user}>"

    def to_csv(self):
        return f"{self.name},{self.amount},{self.category},{self.date},{self.user}"

    @staticmethod
    def from_csv(csv_line: str):
        try:
            name, amount, category, date, user = csv_line.strip().split(",")
            return Expense(name, float(amount), category, date, user)
        except ValueError:
            raise ValueError(f"Invalid CSV line: {csv_line}")


class SavingsGoal:
    def __init__(self, name: str, target_amount: float, deadline: str, user: str):
        self.name = name
        self.target_amount = target_amount
        self.deadline = deadline  # Format: YYYY-MM-DD
        self.user = user

    def __str__(self):
        return f"{self.name} | Target: ${self.target_amount:.2f} | Deadline: {self.deadline} | User: {self.user}"

    def __repr__(self):
        return f"<SavingsGoal name='{self.name}' target_amount={self.target_amount:.2f} deadline='{self.deadline}' user='{self.user}'>"

    def to_csv(self):
        return f"{self.name},{self.target_amount},{self.deadline},{self.user}"

    @staticmethod
    def from_csv(csv_line: str):
        try:
            name, target_amount, deadline, user = csv_line.strip().split(",")
            return SavingsGoal(name, float(target_amount), deadline, user)
        except ValueError:
            raise ValueError(f"Invalid CSV line: {csv_line}")
