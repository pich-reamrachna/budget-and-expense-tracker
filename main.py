from customtkinter import *
from home_tab import HomeTab
from budget_tab import BudgetTab
from summary_tab import SummaryTab
from data_handler import load_transactions_from_file, load_budgets
from datetime import datetime

class BudgetApp(CTk): 
    def __init__(self):
        super().__init__() 
        self.geometry("1000x1000")
        set_appearance_mode("dark")
        
        # Initialize data
        self.transactions = []
        self.budgets = {}
        self.total_balance = 0.0
        self.total_income = 0.0
        self.total_expense = 0.0
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        
        # Load data
        load_transactions_from_file(self)
        load_budgets(self)
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        self.tabview = CTkTabview(master=self, width=1000, height=1000)
        self.tabview.pack(padx=20, pady=20)

        self.tabview.add("Home")
        self.tabview.add("Budget")
        self.tabview.add("Summary")
        
        # Create tabs
        self.home_tab = HomeTab(self)  
        self.budget_tab = BudgetTab(self)
        self.summary_tab = SummaryTab(self)

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()

