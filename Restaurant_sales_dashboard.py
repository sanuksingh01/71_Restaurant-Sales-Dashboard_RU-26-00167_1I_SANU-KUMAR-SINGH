import pandas as pd
import matplotlib.pyplot as plt


def show(number):
    if number == int(number):
        return int(number)
    return round(number, 2)


def load_data(file_name):
    try:
        data = pd.read_csv(file_name, dtype=str)
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")
        return None

    good_rows = []
    for i in range(len(data)):
        row_number = i + 2
        row = data.iloc[i]
        try:
            quantity = float(row["Quantity"])
        except ValueError:
            print(f"Warning: Row {row_number} skipped - Quantity must be a number.")
            continue
        try:
            price = float(row["Price"])
        except ValueError:
            print(f"Warning: Row {row_number} skipped - Price must be a number.")
            continue
        good_rows.append([row["Date"], row["Item"], row["Category"], quantity, price])

    clean = pd.DataFrame(
        good_rows, columns=["Date", "Item", "Category", "Quantity", "Price"]
    )
    if len(clean) == 0:
        print("Error: No valid rows found.")
        return None
    clean["Sales"] = clean["Quantity"] * clean["Price"]
    return clean


def sales_by_category(data):
    result = data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    print("\nSales by Category")
    for category in result.index:
        print(f"{category} : Rs. {show(result[category])}")
    print(f"Total sales: Rs. {show(data["Sales"].sum())}")


def top_items(data):
    by_item = data.groupby("Item")[["Quantity", "Sales"]].sum()
    top_qty = by_item["Quantity"].idxmax()
    top_rev = by_item["Sales"].idxmax()
    qty = by_item["Quantity"].max()
    if qty == 1:
        word = "unit"
    else:
        word = "units"
    print("\nTop Items")
    print(f"Total sales: Rs. {show(data['Sales'].sum())}")
    print(f"Top item by quantity: {top_qty} ({show(qty)} {word})")
    print(f"Top item by revenue: {top_rev} (Rs. {show(by_item['Sales'].max())})")


def daily_sales(data):
    by_date = data.groupby("Date")["Sales"].sum()
    print("\nDaily Sales")
    for date in by_date.index:
        print(f"{date} : Rs. {show(by_date[date])}")
    print(f"Best day: {by_date.idxmax()}")


def show_charts(data):
    by_category = data.groupby("Category")["Sales"].sum()
    by_date = data.groupby("Date")["Sales"].sum()
    by_item = data.groupby("Item")["Sales"].sum()

    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    plt.bar(by_category.index, by_category.values)
    plt.title("Sales by Category")

    plt.subplot(1, 3, 2)
    plt.plot(by_date.index, by_date.values, marker="o")
    plt.title("Sales by Date")

    plt.subplot(1, 3, 3)
    plt.bar(by_item.index, by_item.values)
    plt.title("Sales by Item")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.savefig("dashboard.png")
    plt.show()


file_name = input("Enter CSV file name (press Enter for restaurant_sales.csv): ")
if file_name == "":
    file_name = "restaurant_sales.csv"

data = load_data(file_name)

if data is not None:
    while True:
        print("\n===== Restaurant Sales Dashboard =====")
        print("1. Sales by category")
        print("2. Top items")
        print("3. Daily sales")
        print("4. Show charts")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            sales_by_category(data)
        elif choice == "2":
            top_items(data)
        elif choice == "3":
            daily_sales(data)
        elif choice == "4":
            show_charts(data)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 to 5.")
