class ExpenseError(Exception):
    """Custom exception class for expense-related errors."""
    pass 


class Expense:
    def __init__(self,name,amount,category):
        self.name = name
        self.amount = amount
        self.category = category


    def __repr__(self):
        return f"Expense : {self.name},{self.amount:.2f},{self.category}"