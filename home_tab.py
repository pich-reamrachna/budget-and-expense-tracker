from customtkinter import *
from tkcalendar import DateEntry
import tkinter
from datetime import datetime
from data_handler import save_transactions_to_file
from utils import change_month
from categories import get_all_categories, CATEGORIES
from warning_box import show_warning

class HomeTab:
    def __init__(self, app):
        self.app = app
        self.tab = app.tabview.tab("Home")
        self.create_widgets()

    def create_widgets(self):
        self.create_month_nav_frame()
        self.create_home_frame()
        self.create_transaction_button()
        self.filter_transactions_by_month()

    def create_month_nav_frame(self):
        self.month_nav_frame = CTkFrame(self.tab)
        self.month_nav_frame.pack(pady=5, padx=5, fill='x')

        self.prev_month_btn = CTkButton(self.month_nav_frame, text="<", width=30, command=lambda: change_month(self.app, -1))
        self.prev_month_btn.pack(side='left', padx=5)

        self.month_label = CTkLabel(self.month_nav_frame, text="", font=("Arial", 14))
        self.month_label.pack(side='left', expand=True)

        self.next_month_btn = CTkButton(self.month_nav_frame, text=">", width=30, command=lambda: change_month(self.app, 1))
        self.next_month_btn.pack(side='right', padx=5)

        self.month_label.configure(text=f"{datetime(self.app.current_year, self.app.current_month, 1).strftime('%B %Y')}")

    def create_home_frame(self):
        self.home_frame = CTkFrame(self.tab)
        self.home_frame.pack(fill='x', pady=2, padx=10)

        # Financial info at top
        info_frame = CTkFrame(self.home_frame)
        info_frame.pack(fill='x', pady=5)

        self.label_balance = CTkLabel(info_frame, text="Balance: $0.00", font=("Arial", 14, 'bold'))
        self.label_balance.pack(anchor = 'w', padx = 20)

        self.label_income = CTkLabel(info_frame, text="Income: $0.00", font=("Arial", 14))
        self.label_income.pack(anchor = 'w', padx = 20)

        self.label_expense = CTkLabel(info_frame, text="Expense: $0.00", font=("Arial", 14))
        self.label_expense.pack(anchor = 'w', padx = 20)

        self.label_history = CTkLabel(self.home_frame, text="Transaction History", font=("Arial", 14))
        self.label_history.pack(pady=10)

    def create_transaction_button(self):
        self.transaction_button = CTkButton(
            master= self.tab,
            text= "Create Transaction",
            command= self.transaction_box,
            fg_color= "#2a9d8f",
            hover_color= "#21867a"
        )
        self.transaction_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

    def transaction_box(self):
        transaction_window = CTkToplevel(self.app)
        transaction_window.geometry("300x300")
        transaction_window.title("Enter your Transaction")

        # Make sure it appears above the main app and stays focused
        transaction_window.transient(self.app)  # Set the main app as its parent
        transaction_window.grab_set()           # Block interaction with main window until closed
        transaction_window.focus()              # Give focus to the new window
        transaction_window.lift() 

        transaction_box_frame = CTkFrame(transaction_window)
        transaction_box_frame.pack(pady=5, padx=5, fill='x')
        transaction_box_frame.grid_columnconfigure(0, weight=0)
        transaction_box_frame.grid_columnconfigure(1, weight=1)

        label_amount = CTkLabel(transaction_box_frame, text="Enter the Amount:", font=("Arial", 13))
        label_amount.grid(row=0, column=0, padx=0, pady=1, sticky='w')

        entry_amount = CTkEntry(transaction_box_frame, width=200)
        entry_amount.grid(row=0, column=1, padx=0, pady=1, sticky='w')

        label_type = CTkLabel(transaction_box_frame, text="Choose the transaction type:", font=("Arial", 13))
        label_type.grid(row=1, column=0, padx=1, pady=1, sticky='w')

        transaction_type = StringVar(value="")

        radio_income = CTkRadioButton(transaction_box_frame, text="Income", variable=transaction_type, value="Income")
        radio_expense = CTkRadioButton(transaction_box_frame, text="Expense", variable=transaction_type, value="Expense")
        radio_income.grid(row=2, column=0, padx=1, pady=1, sticky='w')
        radio_expense.grid(row=2, column=1, padx=1, pady=1, sticky='w')

        category_options = get_all_categories()
        subcategory_map = CATEGORIES

        label_category = CTkLabel(transaction_box_frame, text='Category', font=("Arial", 13))
        label_category.grid(row=3, column=0, padx=1, pady=1, sticky='w')

        category_var = StringVar(value='')
        category_dropdown = CTkOptionMenu(transaction_box_frame, values=category_options, variable=category_var, height=20)
        category_dropdown.grid(row=3, column=1, padx=1, pady=1, sticky='w')

        label_subcategory = CTkLabel(transaction_box_frame, text='Subcategory', font=("Arial", 13))
        label_subcategory.grid(row=4, column=0, padx=1, pady=1, sticky='w')

        subcategory_var = StringVar(value='Select')
        subcategory_dropdown = CTkOptionMenu(transaction_box_frame, values=["Select"], variable=subcategory_var, height=20)
        subcategory_dropdown.grid(row=4, column=1, padx=1, pady=1, sticky='w')

        def update_subcategories(*args):
            selected_cat = category_var.get()
            subcategories = subcategory_map.get(selected_cat, ["Select"])
            subcategory_dropdown.configure(values=subcategories)
            subcategory_var.set(subcategories[0])

        def toggle_category(*args):
                    if transaction_type.get() == "Income":
                        label_category.grid_remove()
                        category_dropdown.grid_remove()
                        label_subcategory.grid_remove()
                        subcategory_dropdown.grid_remove()
                    else:
                        label_category.grid()
                        category_dropdown.grid()
                        label_subcategory.grid()
                        subcategory_dropdown.grid()

        category_var.trace_add("write", update_subcategories)
        transaction_type.trace_add("write", toggle_category)
                
        label_date = CTkLabel(transaction_box_frame, text="Choose Date:", font=("Arial", 13))
        label_date.grid(row=5, column=0, padx=1, pady=1, sticky='w')

        date_frame = tkinter.Frame(transaction_box_frame)
        date_frame.grid(row=5, column=1, padx=1, pady=1, sticky='w')
        date_picker = DateEntry(date_frame, width=15, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_picker.pack()

        def save_transaction():
            amount_str = entry_amount.get().strip()
            trans_type = transaction_type.get()
            date = date_picker.get()

            if not amount_str or not trans_type or not date:
                show_warning("Amount, Type, and Date are required!")
                return 
            
            try:
                amount = float(amount_str)
            except ValueError:
                print("Invalid amount format!")
                return
            
            category = ""
            subcategory = ""
            
            if trans_type == "Expense":
                category = category_var.get()
                subcategory = subcategory_var.get()
                if not category or subcategory == "Select":
                    show_warning("Category and Subcategory are required for expenses!")
                    return

            data = {
                "amount": amount,
                "type": trans_type,
                "category": category,
                "subcategory": subcategory,
                "date": date
            }

            self.app.transactions.append(data)
            save_transactions_to_file(self.app)
            self.filter_transactions_by_month()
            self.app.budget_tab.update_budget_display()
            self.app.summary_tab.update_summary_chart()
            transaction_window.destroy()

        save_button = CTkButton(transaction_box_frame, text="Save", command=save_transaction, fg_color="#2a9d8f", hover_color="#21867a")
        save_button.grid(row=6, column=0, columnspan=2, pady=10)
 
    def update_balance_color(self, balance):
            if balance < 0:
                self.label_balance.configure(text_color = 'red')
            else:
                self.label_balance.configure(text_color='white')

    def filter_transactions_by_month(self):
        self.app.total_balance = 0.0
        self.app.total_income = 0.0
        self.app.total_expense = 0.0

        for widget in self.tab.winfo_children():
            if isinstance(widget, CTkFrame) and widget not in [self.home_frame, self.month_nav_frame]:
                widget.destroy()
        
        has_transactions = False

        for i, trans in enumerate(self.app.transactions):
            trans_date = datetime.strptime(trans["date"], "%Y-%m-%d")
            if trans_date.month == self.app.current_month and trans_date.year == self.app.current_year:
                has_transactions = True
                amount = trans["amount"]
                trans_type = trans["type"]
                category = trans["category"]
                subcategory = trans["subcategory"]
                date = trans["date"]

                trans_frame = CTkFrame(self.tab)
                trans_frame.pack(pady=2, fill='x', padx=5)

                if trans_type == "Income":
                    text = f"{trans_type} - ${amount:.2f} on {date}"
                    CTkLabel(trans_frame, text=text, text_color = 'green').pack(side='left', padx=5)
                    self.app.total_income += amount
                    self.app.total_balance += amount
                else:
                    text = f"{trans_type} - ${amount:.2f} on {date} ({category}/{subcategory})"
                    CTkLabel(trans_frame, text=text, text_color = 'red').pack(side='left', padx=5)
                    self.app.total_expense += amount
                    self.app.total_balance -= amount

                delete_btn = CTkButton(
                    trans_frame,
                    text="X",
                    width=20,
                    fg_color="red",
                    hover_color="darkred",
                    command=lambda idx=i, frame=trans_frame: self.delete_transaction(idx, frame)
                )
                delete_btn.pack(side='right', padx=5)

                edit_btn = CTkButton(
                    trans_frame,
                    text="Edit",
                    width=20,
                    fg_color='blue',
                    hover_color='darkblue',
                    command=lambda idx=i: self.edit_transaction(idx)
                )
                edit_btn.pack(side='right', padx=5)

        if not has_transactions:
            no_data_frame = CTkFrame(self.tab)
            no_data_frame.pack(pady = 20, padx = 10, fill = 'x')
            CTkLabel(no_data_frame, text = 'No Income or Expense for this month.', font=('Arial', 14), text_color = "gray").pack(pady =10)

        self.label_balance.configure(text=f"Balance: ${self.app.total_balance:.2f}")
        self.label_income.configure(text=f"Income: ${self.app.total_income:.2f}")
        self.label_expense.configure(text=f"Expense: ${self.app.total_expense:.2f}")
        self.update_balance_color(self.app.total_balance)

    def delete_transaction(self, transaction_index, transaction_frame):
        trans = self.app.transactions[transaction_index]

        if trans["type"] == "Income":
            self.app.total_income -= trans["amount"]
            self.app.total_balance -= trans["amount"]
        else:
            self.app.total_expense -= trans["amount"]
            self.app.total_balance += trans["amount"]

        del self.app.transactions[transaction_index]
        save_transactions_to_file(self.app)
        transaction_frame.destroy()

        self.label_balance.configure(text=f"Balance: ${self.app.total_balance:.2f}")
        self.label_income.configure(text=f"Income: ${self.app.total_income:.2f}")
        self.label_expense.configure(text=f"Expense: ${self.app.total_expense:.2f}")
        self.update_balance_color(self.app.total_balance)

        self.app.budget_tab.update_budget_display()
        self.app.summary_tab.update_summary_chart()

    def edit_transaction(self, transaction_index):
        transaction = self.app.transactions[transaction_index]

        # Create the edit window
        edit_window = CTkToplevel(self.app)
        edit_window.geometry("300x350")
        edit_window.title("Edit Transaction")

        edit_window.transient(self.app)  # Set the main app as its parent
        edit_window.grab_set()           # Block interaction with main window until closed
        edit_window.focus()              # Give focus to the new window
        edit_window.lift() 

        edit_frame = CTkFrame(edit_window)
        edit_frame.pack(pady=5, padx=5, fill='x')
        edit_frame.grid_columnconfigure(0, weight=0)
        edit_frame.grid_columnconfigure(1, weight=1)

        # Pre-fill current values
        label_amount = CTkLabel(edit_frame, text="Amount:", font=("Arial", 13))
        label_amount.grid(row=0, column=0, padx=0, pady=1, sticky='w')

        entry_amount = CTkEntry(edit_frame, width=200)
        entry_amount.grid(row=0, column=1, padx=0, pady=1, sticky='w')
        entry_amount.insert(0, str(transaction["amount"]))

        label_type = CTkLabel(edit_frame, text="Type:", font=("Arial", 13))
        label_type.grid(row=1, column=0, padx=1, pady=1, sticky='w')

        transaction_type = StringVar(value=transaction["type"])

        radio_income = CTkRadioButton(edit_frame, text="Income", variable=transaction_type, value="Income")
        radio_expense = CTkRadioButton(edit_frame, text="Expense", variable=transaction_type, value="Expense")
        radio_income.grid(row=2, column=0, padx=1, pady=1, sticky='w')
        radio_expense.grid(row=2, column=1, padx=1, pady=1, sticky='w')

        category_options = get_all_categories()
        subcategories_dict = CATEGORIES

        category_var = StringVar(value=transaction["category"])
        subcategory_var = StringVar(value=transaction["subcategory"])

        label_category = CTkLabel(edit_frame, text="Category", font=("Arial", 13))
        label_category.grid(row=3, column=0, padx=1, pady=1, sticky='w')

        category_dropdown = CTkOptionMenu(edit_frame, values=category_options, variable=category_var, height=20)
        category_dropdown.grid(row=3, column=1, padx=1, pady=1, sticky='w')

        label_subcategory = CTkLabel(edit_frame, text='Subcategory', font=("Arial", 13))
        label_subcategory.grid(row=4, column=0, padx=1, pady=1, sticky='w')

        initial_category = category_var.get()
        initial_subcategories = subcategories_dict.get(initial_category, ["Select"])

        subcategory_dropdown = CTkOptionMenu(edit_frame, values=initial_subcategories, variable=subcategory_var, height=20)
        subcategory_dropdown.grid(row=4, column=1, padx=1, pady=1, sticky='w')
        
        def update_subcategories(*args):
            selected_cat = category_var.get()
            new_subcategories = subcategories_dict.get(selected_cat, ["Select"])
            subcategory_dropdown.configure(values=new_subcategories)
            subcategory_var.set(new_subcategories[0])

        def toggle_category(*args):
            if transaction_type.get() == "Income":
                label_category.grid_remove()
                category_dropdown.grid_remove()
                label_subcategory.grid_remove()
                subcategory_dropdown.grid_remove()
            else:
                label_category.grid()
                category_dropdown.grid()
                label_subcategory.grid()
                subcategory_dropdown.grid()

        category_var.trace_add("write", update_subcategories)
        transaction_type.trace_add("write", toggle_category)

        toggle_category()

        label_date = CTkLabel(edit_frame, text="Choose Date:", font=("Arial", 13))
        label_date.grid(row=5, column=0, padx=1, pady=1, sticky='w')

        date_frame = tkinter.Frame(edit_frame)
        date_frame.grid(row=5, column=1, padx=1, pady=1, sticky='w')
        date_picker = DateEntry(date_frame, width=15, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_picker.set_date(transaction["date"])
        date_picker.pack()
        
        def save_edited_transaction():
            new_amount = entry_amount.get().strip()
            new_transaction_type = transaction_type.get()
            # new_category = category_var.get()
            # new_subcategory = subcategory_var.get()
            new_date = date_picker.get()

            if not new_amount or not new_transaction_type or not new_date:
                show_warning("Amount, Type, and Date are required!")
                return 
            
            try:
                new_amount = float(new_amount)
            except ValueError:
                print("Invalid amount format!")
                return  
            
            new_category = ""
            new_subcategory = ""

            if new_transaction_type == "Expense":
                new_category = category_var.get()
                new_subcategory = subcategory_var.get()
                if not new_category or new_subcategory == "Select":
                    show_warning("Category and Subcategory are required for Expenses!")
                    return

                # Update the transaction data
            self.app.transactions[transaction_index] = {
                "amount": new_amount,
                "type": new_transaction_type,
                "category": new_category,
                "subcategory": new_subcategory,  
                "date": new_date
            }

            save_transactions_to_file(self.app)
            self.filter_transactions_by_month()
            self.app.budget_tab.update_budget_display()
            self.app.summary_tab.update_summary_chart()
            edit_window.destroy()
        

        save_button = CTkButton(edit_frame, text="Save Changes", command=save_edited_transaction, fg_color="#2a9d8f", hover_color="#21867a")
        save_button.grid(row=6, column=0, columnspan=2, pady=10)
