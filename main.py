import json
import argparse


def add_expense(budget, expenses, description, amount):
    if budget < amount:
        print("Невозможно добавить трату, у вас слишком мало денег.")
        return budget, expenses
    else:
        print(f"Добавлена трата: {description}, потрачено денег: {amount}")
        expenses[description] = amount
        return budget - amount, expenses


def get_total_expenses(expenses):
    return sum(expenses.values())


def show_budget_details(first_budget, budget, additional_budget, expenses):
    print(f"\nТекущий баланс: {budget}")
    print("Траты: ")
    expenses_names = list(expenses.keys())
    for expense_name in expenses_names:
        print(f" - {expense_name}: {expenses[expense_name]}")
    print(f"Всего потрачено: {get_total_expenses(expenses)}")
    print(f"Добавлено к балансу: {additional_budget}")
    print(f"Начальный бюджет: {first_budget}")


def save_budget_details(initial_budget, expenses, first_budget, additional_budget, filepath):
    data = {
        "initial_budget": initial_budget,
        "first_budget": first_budget,
        "additional_budget": additional_budget,
        "expenses": expenses
    }
    with open(filepath, "w") as file:
        json.dump(data, file, ensure_ascii=False)


def load_budget_data(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
            if data["initial_budget"] > 0:
                show_budget_details(data["first_budget"], data["initial_budget"], 0, data["expenses"])
                return data["initial_budget"], data["first_budget"],data["additional_budget"], data["expenses"]
            else:
                first_budget = float(input("Пожалуйста, введите имеющееся у вас кол-во денег: "))
                return first_budget, first_budget, data["additional_budget"], data["expenses"]
    except FileNotFoundError:
        first_budget = float(input("Пожалуйста, введите имеющееся у вас кол-во денег: "))
        return first_budget, first_budget, 0, {}
    except json.JSONDecodeError:
        first_budget = float(input("Пожалуйста, введите имеющееся у вас кол-во денег: "))
        return first_budget, first_budget, 0, {}


def update_budget(budget):
    additional_budget = float(input("Введите полученную сумму: "))
    return additional_budget, budget + additional_budget


def main():
    parser = argparse.ArgumentParser(prog="budget counter", description="Данная программа может быть использоована для подсчета бюджета.")
    parser.add_argument("-f", "--filepath", help="Введите путь до файла с данными.", required=False, default="data.json")
    args = parser.parse_args()
    filepath = args.filepath
    print("Добро пожаловать, здесь вы сможете отслеживать ваши финансы.\n")
    initial_budget, first_budget, additional_budget, expenses = load_budget_data(filepath)
    budget = initial_budget
    while True:
        current_choice = input("\nЧто бы вы хотели сделать?\n1. Добаить траты;\n2. Показать кол-во оставшихся денег;\n3. Обновить бюджет;\n4. Выйти\nВаш выбор 1/2/3/4: ")
        if current_choice == "1":
            budget, expenses = add_expense(budget, expenses, input("\nВведите описание траты: "), float(input("Введите стоимость покупки: ")))
        elif current_choice == "2":
            show_budget_details(first_budget, budget, additional_budget, expenses)
        elif current_choice == "3":
            additional_budget, budget = update_budget(budget)
        elif current_choice == "4":
            print("\nСпасибо, что воспользовались нашим приложением.\nДо свидания!")
            save_budget_details(budget, expenses, first_budget, additional_budget, filepath)
            break


if __name__ == "__main__":
    main()