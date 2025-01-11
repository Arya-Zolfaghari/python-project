import tkinter as tk
from tkinter import messagebox, Button
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import sqlite3





# Create main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("1920x1080")  # Set window size

# Data variables
expenses_data = []
income_data = []  # To store income data
categories = ["Food", "Entertainment", "Transport", "Bills", "Others"]
category_colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]
frame_charts = None


# ==================================================  DATA BACE  =======================================================
conn = sqlite3.connect("Money_manager.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    description TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('Expense', 'Income')) NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
''')


for category in categories:
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))
conn.commit()


# __________________________________________________________________________________________________________________________
# __________________________________________________________________________________________________________________________
# __________________________________________________________________________________________________________________________



def add_data():
    try:
        amount = float(entry_amount.get())
        description = entry_description.get()
        category = entry_category.get()
        type_ = entry_type.get()
        date_today = datetime.date.today().strftime("%Y-%m-%d")

        if amount <= 0 or not description:
            raise ValueError("Amount must be greater than zero and description can't be empty.")

        # پیدا کردن یا اضافه کردن دسته‌بندی
        cursor.execute("SELECT id FROM categories WHERE name = ?", (category,))
        category_id = cursor.fetchone()
        if not category_id:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))
            category_id = cursor.lastrowid
        else:
            category_id = category_id[0]

        cursor.execute('''
            INSERT INTO transactions (amount, description, category_id, type, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (amount, description, category_id, type_, date_today))
        conn.commit()

        if type_ == "Expense":
            expenses_data.append((category, description, amount, date_today))
            tree.insert("", "end", values=(category, description, amount, date_today))
        else:
            income_data.append(("Income", description, amount, date_today))
            messagebox.showinfo("Info", "Income data recorded successfully (not displayed in the table).")

        entry_amount.delete(0, tk.END)
        entry_description.delete(0, tk.END)
        update_summary()

    except ValueError as e:
        messagebox.showerror("Error", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Database Error: {e}")



# __________________________________________________________________________________________________________________________


def update_summary():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Expense'")
    total_expenses = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Income'")
    total_income = cursor.fetchone()[0] or 0

    remaining = total_income - total_expenses

    label_total_expenses.config(text=f"Total Expenses: {total_expenses} Toman")
    label_total_income.config(text=f"Total Income: {total_income} Toman")
    label_remaining.config(text=f"Remaining Money: {remaining} Toman")


# __________________________________________________________________________________________________________________________



def clear_chart_area():
    if frame_charts:
        for widget in frame_charts.winfo_children():
            widget.destroy()



# __________________________________________________________________________________________________________________________




def show_weekly_chart():
    clear_chart_area()

    amounts = [amount for _, _, amount, _ in expenses_data]
    descriptions = [description for _, description, _, _ in expenses_data]

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    wedges, texts, autotexts = ax.pie(amounts, labels=descriptions, colors=category_colors[:len(descriptions)],
                                      autopct='%1.1f%%', startangle=90)

    for i, text in enumerate(texts):
        text.set_text(f"{descriptions[i]}: {amounts[i]} Toman")
        text.set_color("black")

    ax.set_title("Weekly Expenses by Description")
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=frame_charts)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=20)

    canvas.draw()



# __________________________________________________________________________________________________________________________



def show_monthly_chart():
    clear_chart_area()

    dates = [date for _, _, _, date in expenses_data]
    total_expenses_per_day = {date: 0 for date in dates}
    for _, _, amount, date in expenses_data:
        total_expenses_per_day[date] += amount

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(list(total_expenses_per_day.keys()), list(total_expenses_per_day.values()), marker='o', color='b')
    ax.set_title("Monthly Expenses")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount (Toman)")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=frame_charts)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=20)

    canvas.draw()



# __________________________________________________________________________________________________________________________




def show_details():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an item from the table first.")
        return

    item = tree.item(selected_item)
    values = item["values"]

    # Only showing expense details
    if values[0] != "Income":  # We avoid showing income details in this case
        category, description, amount, date = values[0], values[1], values[2], values[3]
        details = f"Category: {category}\nDescription: {description}\nAmount: {amount} Toman\nDate: {date}"

        details_window = tk.Toplevel(root)
        details_window.title("Details")
        details_label = tk.Label(details_window, text=details, font=("Helvetica", 12))
        details_label.pack(padx=20, pady=20)
        details_window.geometry("300x250")



# __________________________________________________________________________________________________________________________




# GUI elements
def main():
    global frame_charts, tree
    clear_chart_area()

    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Inputs
    tk.Label(frame, text="Amount (Toman):").grid(row=0, column=0)
    global entry_amount
    entry_amount = tk.Entry(frame)
    entry_amount.grid(row=0, column=1)

    tk.Label(frame, text="Description (e.g., Restaurant, Transport):").grid(row=1, column=0)
    global entry_description
    entry_description = tk.Entry(frame)
    entry_description.grid(row=1, column=1)

    global entry_type
    entry_type = tk.StringVar(value="Expense")
    tk.Radiobutton(frame, text="Expense", variable=entry_type, value="Expense").grid(row=2, column=0)
    tk.Radiobutton(frame, text="Income", variable=entry_type, value="Income").grid(row=2, column=1)

    global entry_category
    tk.Label(frame, text="Category:").grid(row=3, column=0)
    entry_category = tk.StringVar(value=categories[0])
    tk.OptionMenu(frame, entry_category, *categories).grid(row=3, column=1)

    # Button to add data
    tk.Button(frame, text="Add Data", command=add_data).grid(row=4, columnspan=2)

    # Summary section
    summary_frame = tk.Frame(root)
    summary_frame.pack(pady=20)

    global label_total_expenses
    label_total_expenses = tk.Label(summary_frame, text="Total Expenses: 0 Toman")
    label_total_expenses.grid(row=0, column=0)

    global label_total_income
    label_total_income = tk.Label(summary_frame, text="Total Income: 0 Toman")
    label_total_income.grid(row=1, column=0)

    global label_remaining
    label_remaining = tk.Label(summary_frame, text="Remaining Money: 0 Toman")
    label_remaining.grid(row=2, column=0)

    # Table for displaying transactions (only expenses are shown)
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10)

    tree = ttk.Treeview(tree_frame, columns=("Category", "Description", "Amount", "Date"), show="headings")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")
    tree.heading("Amount", text="Amount")
    tree.heading("Date", text="Date")
    tree.pack()

    # Buttons for weekly and monthly charts
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=10)

    frame_charts = tk.Frame(root)
    frame_charts.pack(pady=10)

    tk.Button(frame_buttons, text="Weekly Chart", command=show_weekly_chart).grid(row=0, column=0, padx=20)
    tk.Button(frame_buttons, text="Monthly Chart", command=show_monthly_chart).grid(row=0, column=1, padx=20)

    # Button to show details
    tk.Button(frame_buttons, text="Show Details", command=show_details).grid(row=0, column=2, padx=20)
    clear_button = Button(root, text="Clear Database", command=clear_database)
    clear_button.pack(pady=10, padx=20)

    # Add close button
    close_button = tk.Button(root, text="Exit", command=root.quit)
    close_button.pack(side="bottom", pady=10)




# ______________________________________________________________________________________________________________________


def clear_database():
    try:
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM categories")
        conn.commit()

        messagebox.showinfo("Success", "All data has been cleared from the database.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# ______________________________________________________________________________________________________________________




# Start program
if __name__ == '__main__':
    main()
    root.mainloop()
