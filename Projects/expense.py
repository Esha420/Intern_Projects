from datetime import datetime
expenses = []
budgets = {}

def validate_date(date_str):
    try:
        entered_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.today().date()

        if entered_date > today:
            print("❌ Date cannot be in the future.")
            return False

        return True
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")
        return False


def set_budget():
    category = input("Enter category to set budget for: ")
    try:
        amount = float(input(f"Set monthly budget for '{category}': Rs."))
        budgets[category] = amount
        print(f"✅ Budget set for '{category}' is Rs.{amount}")
    except ValueError:
        print("❌ Invalid amount. Try again.")

def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    if not validate_date(date):
        print("❌ Invalid Date.")
        return
    category = input("Enter category: ")
    try:
        amount = float(input("Enter amount: Rs."))
    except ValueError:
        print("❌ Invalid amount. Try again.")
        return

    expenses.append({"date": date, "category": category, "amount": amount})
    print("✅ Expense added.")

    # Budget check
    total_in_category = sum(exp['amount'] for exp in expenses if exp['category'] == category)
    if category in budgets:
        if total_in_category > budgets[category]:
            print(f"⚠️ Warning: You've exceeded the budget for '{category}' (₹{budgets[category]})")
        else:
            print(f"🧮 Spent ₹{total_in_category} of ₹{budgets[category]} in '{category}'")

def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return
    print("\n📊 Expense History:")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['date']} | {exp['category']} | Rs.{exp['amount']}")

def view_by_category():
    if not expenses:
        print("No expenses yet.")
        return

    print("\n📂 Expenses by Category:")
    categories = set(exp['category'] for exp in expenses)
    for cat in categories:
        total = sum(exp['amount'] for exp in expenses if exp['category'] == cat)
        print(f"- {cat}: Rs.{total}")

def delete_expense():
    view_expenses()
    if not expenses:
        return
    try:
        index = int(input("Enter the number of the expense to delete: ")) - 1
        removed = expenses.pop(index)
        print(f"🗑️ Deleted: {removed}")
    except (ValueError, IndexError):
        print("❌ Invalid selection.")

def main():
    while True:
        print("\n🔹 Expense Tracker CLI")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Expenses by Category")
        print("4. Set Budget")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            view_by_category()
        elif choice == '4':
            set_budget()
        elif choice == '5':
            delete_expense()
        elif choice == '6':
            print("Bye! 🧾 Happy tracking 💸")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
