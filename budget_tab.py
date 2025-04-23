from customtkinter import *
from data_handler import save_budgets
from utils import update_month_display, change_month
from datetime import datetime
from categories import get_all_categories

class BudgetTab:
    def __init__(self, app):
        self.app = app
        self.tab = app.tabview.tab("Budget")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_month_nav_frame()
        self.update_budget_display()
        
    def create_month_nav_frame(self):
        self.month_nav_frame = CTkFrame(self.tab)
        self.month_nav_frame.pack(pady=5, padx=5, fill='x')

        self.prev_month_btn = CTkButton(self.month_nav_frame, text="<", width=30, command=lambda: change_month(self.app, -1))
        self.prev_month_btn.pack(side='left', padx=5)

        self.month_label = CTkLabel(self.month_nav_frame, text="", font=("Arial", 14))
        self.month_label.pack(side='left', expand=True)

        self.next_month_btn = CTkButton(self.month_nav_frame, text=">", width=30, command=lambda: change_month(self.app, 1))
        self.next_month_btn.pack(side='right', padx=5)

        update_month_display(self.app)
    
    def create_budget_frame(self, total_budget, total_expense):
        self.budget_frame = CTkFrame(self.tab)
        self.budget_frame.pack(fill='x', pady=2, padx=10)

        self.info_frame = CTkFrame(self.budget_frame)
        self.info_frame.pack(fill='x', pady=5)

        self.label_budget = CTkLabel(self.info_frame, text=f"Total Budget: ${total_budget:.2f}", font=("Arial", 14))
        self.label_budget.pack(anchor = 'w', padx = 20)

        self.label_expenses = CTkLabel(self.info_frame, text=f"Total Expenses: ${total_expense:.2f}", font=("Arial", 14))
        self.label_expenses.pack(anchor = 'w',  padx = 20)

        remaining = total_budget - total_expense
        color = "green" if remaining >= 0 else "red"
        
        self.label_remaining = CTkLabel(self.info_frame, text=f"Remaining: ${remaining:.2f}", font=("Arial", 14, 'bold'), text_color = color)
        self.label_remaining.pack(anchor = 'w',  padx = 20)

        self.label_categories = CTkLabel(self.budget_frame, text="Categories", font=("Arial", 14))
        self.label_categories.pack(pady=10)

    def update_budget_display(self):
        for widget in self.tab.winfo_children():
            if widget not in [self.month_nav_frame]:
                widget.destroy()

        month_key = f"{self.app.current_year}-{self.app.current_month:02d}"
        month_budgets = self.app.budgets.get(month_key, {})
        
        category_expenses = {category: 0 for category in get_all_categories()}
        
        for trans in self.app.transactions:
            trans_date = datetime.strptime(trans["date"], "%Y-%m-%d")
            if (trans_date.month == self.app.current_month and trans_date.year == self.app.current_year and trans["type"] == "Expense"):
                category = trans["category"]
                if category in category_expenses:
                    category_expenses[category] += trans["amount"]

        total_budget = sum(month_budgets.values())
        total_expense = sum(category_expenses.values())

        self.create_budget_frame(total_budget, total_expense)

        for category in get_all_categories():
            category_frame = CTkFrame(self.tab)
            category_frame.pack(pady=5, padx=10, fill='x')
            
            budget = month_budgets.get(category, 0)
            expense = category_expenses.get(category, 0)
            remaining = budget - expense
            
            CTkLabel(category_frame, text=f"{category}:", font=("Arial", 13, 'bold')).pack(anchor='w')
            CTkLabel(category_frame, text=f"Budget: ${budget:.2f}").pack(anchor='w')
            CTkLabel(category_frame, text=f"Expense: ${expense:.2f}").pack(anchor='w')
            CTkLabel(category_frame, text=f"Remaining: ${remaining:.2f}", 
                    text_color="green" if remaining >= 0 else "red").pack(anchor='w')

        CTkButton(self.tab, text="Set Budget", command=self.set_budget_window, fg_color="#2a9d8f").pack(pady=10)
        
    def set_budget_window(self):
        budget_window = CTkToplevel(self.app)
        budget_window.geometry("300x250")
        budget_window.title("Set Budget")

        budget_window.transient(self.app)  # Set the main app as its parent
        budget_window.grab_set()           # Block interaction with main window until closed
        budget_window.focus()              # Give focus to the new window
        budget_window.lift()
        
        budget_frame = CTkFrame(budget_window)
        budget_frame.pack(pady=10, padx=10, fill='both', expand=True)

        CTkLabel(budget_frame, text="Category:", font=("Arial", 13)).pack(pady=5)
        category_var = StringVar(value=get_all_categories()[0])
        category_menu = CTkOptionMenu(budget_frame, values=get_all_categories(), variable=category_var)
        category_menu.pack(pady=5)

        CTkLabel(budget_frame, text="Budget Amount:", font=("Arial", 13)).pack(pady=5)
        amount_entry = CTkEntry(budget_frame)
        amount_entry.pack(pady=5)

        def save_budget():
            try:
                amount = float(amount_entry.get())
                category = category_var.get()
                
                month_key = f"{self.app.current_year}-{self.app.current_month:02d}"
                if month_key not in self.app.budgets:
                    self.app.budgets[month_key] = {}
                
                self.app.budgets[month_key][category] = amount
                save_budgets(self.app)
                self.update_budget_display()
                self.app.summary_tab.update_summary_chart()
                budget_window.destroy()
            except ValueError:
                print("Please enter a valid number")

        CTkButton(budget_frame, text="Set Budget", command=save_budget, fg_color="#2a9d8f").pack(pady=10)