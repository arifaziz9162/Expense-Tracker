from ex import Expense,ExpenseError
import calendar
import datetime
import logging

# File handler and stream handler setup
logger = logging.getLogger("Expense_Logger")
logger.setLevel(logging.DEBUG)

if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)  
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("expense_tracker.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def main():
    print("Program Started.")
    expense_file_path = "expense.csv"
    budget = 30000

    try:

        expense = get_expense_info()
        save_to_file(expense,expense_file_path )
        summarize_expenses(expense_file_path,budget)
        
    except ExpenseError as e:
        logger.error(f"Unexpected error occured : {e}")


def get_expense_info():
    print("How much did you spend ?")

    try:

        expense_name = input("Where did you spend : ")
        expense_amount = float(input("How much money was spend here : "))
        if not isinstance(expense_name,str):
            raise TypeError("Expense name must be a string.")
        
    except ValueError as e:
        logger.error(f"Invalid input! {e}")
        raise ExpenseError(e)

    print(f"Expense name is {expense_name} and Expense amount is {expense_amount}")


    expense_categories = [
        "🥙 Food",
        "🏡 Home",
        "🏢 Work",
        "🎉 Fun",
        "✨Miscellaneous"
    ]


    while True:
        print("Select a category for this expense : ")
        for i , category_name in enumerate(expense_categories):
            print(f"{i+1}.{category_name}")

        try:

            value_range = f"[1-{len(expense_categories)}]"
            selected_index = int(input(f"Please tell the category {value_range} : "))-1
            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                print(f"selected_category : {selected_category}")
                new_expense = Expense(name = expense_name,category = selected_category , amount = expense_amount)
                return new_expense
            
            else:
                print("Invalid category! Please try again.")

        except ValueError as e:
            logger.error("Invalid input for category selection. Expected a number between 1 to 5")
            raise ExpenseError(e)


def save_to_file(expense,expense_file_path ):
    try:

        logger.info(f"Saving expense to file : {expense} to {expense_file_path}")
        with open(expense_file_path,"a",encoding="utf-8") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")

    except Exception as e:
        logger.error(f"Failed to write to file : {e}")
        raise ExpenseError(e)


def summarize_expenses(expense_file_path,budget):
    logger.info("Summarizing expenses : ")
    expenses = []
    try:

        with open(expense_file_path,"r",encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                print(f"{expense_name} , {expense_amount} and {expense_category}")
                line_expense =Expense(
                    name = expense_name, 
                    amount = float(expense_amount), 
                    category = expense_category
                )
                expenses.append(line_expense)

    except Exception as e:
        logger.error(f"Error reading expenses from file : {e}")
        raise ExpenseError(e)
        

    amount_by_category = {}
    for expense in expenses:
        key = expense.category

        if key in amount_by_category:
            amount_by_category[key] += expense.amount

        else:
            amount_by_category[key] = expense.amount

    print("\nExpense by category: ")
    for key,amount in amount_by_category.items():
        print(f"{key} : {amount}")


    total_spend = sum([x.amount for x in expenses])
    print(f"Total expense : {total_spend:.2f}")


    remaining_budget = budget - total_spend
    print(f"Remaining budget : {remaining_budget}")

    percentage_spent = (total_spend / budget) * 100

    if percentage_spent > 100:
        print("Your expenses have exceeded the budget! Please be cautious.")

    elif percentage_spent > 90:
        print("You are very close to exceeding your budget.")

    elif percentage_spent > 70:
        print("Spending is rising. Be careful.")

    else:
        print("Budget is under control. Good job!")


    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year,now.month)[1]
    remaining_days = days_in_month - now.day
    print(f"Remaining days in this month  : {remaining_days}")

    try:

        daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0
        print(f"Daily  available budget is : {daily_budget:.2f}")

    except ZeroDivisionError:
        logger.warning("No days remaining in this month to calculate daily budget.")
        raise ExpenseError


if __name__ == "__main__":
    main()