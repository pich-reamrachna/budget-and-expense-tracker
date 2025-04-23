from customtkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
from datetime import datetime
from utils import update_month_display, change_month

class SummaryTab:
    def __init__(self, app):
        self.app = app
        self.tab = app.tabview.tab("Summary")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_month_nav_frame()
        self.create_sub_tabs()
        self.tab.after(100, self.update_summary_chart)

    def create_month_nav_frame(self):
        self.month_nav_frame = CTkFrame(self.tab)
        self.month_nav_frame.pack(pady=5, padx=5, fill='x')

        self.prev_month_btn = CTkButton(self.month_nav_frame, text="<", width=30, command=lambda: change_month(self.app, -1))
        self.prev_month_btn.pack(side='left', padx=5)

        self.month_label = CTkLabel(self.month_nav_frame, text="", font=("Arial", 14))
        self.month_label.pack(side='left', expand=True)

        self.next_month_btn = CTkButton(self.month_nav_frame, text=">", width=30, command=lambda: change_month(self.app, 1))
        self.next_month_btn.pack(side='right', padx=5)
        
        
    def create_sub_tabs(self):
        self.sub_tabview = CTkTabview(self.tab)
        self.sub_tabview.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.daily_trends_tab = self.sub_tabview.add("Daily Trends")
        self.expense_breakdown_tab = self.sub_tabview.add("Expense Breakdown")
        self.budget_vs_actual_tab = self.sub_tabview.add("Budget vs Actual Expense")
        
        self.update_summary_chart()
        
    def update_summary_chart(self):
        update_month_display(self.app)
        self.update_daily_trends_tab()
        self.update_expense_breakdown_tab()
        self.update_budget_vs_actual_tab()
        
    def update_daily_trends_tab(self):
        for widget in self.daily_trends_tab.winfo_children():
            widget.destroy()
            
        days_in_month = calendar.monthrange(self.app.current_year, self.app.current_month)[1]
        income_by_day = {day: 0 for day in range(1, days_in_month + 1)}
        expense_by_day = {day: 0 for day in range(1, days_in_month + 1)}
        
        has_transactions = False

        for trans in self.app.transactions:
            trans_date = datetime.strptime(trans["date"], "%Y-%m-%d")
            if trans_date.month == self.app.current_month and trans_date.year == self.app.current_year:
                day = trans_date.day
                if trans["type"] == "Income":
                    income_by_day[day] += trans["amount"]
                    has_transactions = True
                else:
                    expense_by_day[day] += trans["amount"]
                    has_transactions = True
        
        if not has_transactions:
            no_data_frame = CTkFrame(self.daily_trends_tab)
            no_data_frame.pack(pady = 20, padx = 10, fill = 'x')
            CTkLabel(no_data_frame, text = 'No Income or Expense data for this month.', font=('Arial', 14), text_color = "gray").pack(pady =10)
            return
        
        fig = Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)
        ax.plot(range(1, days_in_month + 1), [income_by_day[day] for day in range(1, days_in_month + 1)], label='Income', color='green', marker='o')
        ax.plot(range(1, days_in_month + 1), [expense_by_day[day] for day in range(1, days_in_month + 1)], label='Expense', color='red', marker='o')
        
        ax.set_title(f"Daily Trends - {datetime(self.app.current_year, self.app.current_month, 1).strftime('%B %Y')}", fontsize = 16)
        ax.set_xlabel('Day of Month', fontsize = 14)
        ax.set_ylabel('Amount ($)', fontsize = 14)
        ax.legend(fontsize = 12)
        ax.tick_params(axis='both', labelsize=12)
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, master=self.daily_trends_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
    def update_expense_breakdown_tab(self):
        for widget in self.expense_breakdown_tab.winfo_children():
            widget.destroy()
            
        expense_categories = {}
        
        for trans in self.app.transactions:
            trans_date = datetime.strptime(trans["date"], "%Y-%m-%d")
            if trans_date.month == self.app.current_month and trans_date.year == self.app.current_year:
                if trans["type"] == "Expense":
                    expense_categories[trans["category"]] = expense_categories.get(trans["category"], 0) + trans["amount"]
                
        if not expense_categories:
            label = CTkLabel(self.expense_breakdown_tab, text="No Expense data for this month.", font=("Arial", 14), text_color = 'gray')
            label.pack(pady=20)
            return

        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(expense_categories.values(), labels=expense_categories.keys(), autopct='%1.1f%%', textprops={'fontsize':14})
        
        for text in texts:
            text.set_fontsize(14)
        for autotext in autotexts:
            autotext.set_fontsize(14)
        
        fig.suptitle(f"Expense Breakdown - {datetime(self.app.current_year, self.app.current_month, 1).strftime('%B %Y')}", fontsize = 16)

        canvas = FigureCanvasTkAgg(fig, master=self.expense_breakdown_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
    def update_budget_vs_actual_tab(self):
        for widget in self.budget_vs_actual_tab.winfo_children():
            widget.destroy()
        
        month_key = f"{self.app.current_year}-{self.app.current_month:02d}"
        month_budgets = self.app.budgets.get(month_key, {})

        # Get actual expenses
        category_expenses = {}
        for trans in self.app.transactions:
            trans_date = datetime.strptime(trans["date"], "%Y-%m-%d")
            if (trans["type"] == "Expense" and trans_date.month == self.app.current_month and trans_date.year == self.app.current_year):
                category = trans["category"]
                category_expenses[category] = category_expenses.get(category, 0) + trans["amount"]
        
        all_budget_categories = set(cat for month in self.app.budgets.values() for cat in month)
        all_expense_categories = set(trans["category"] for trans in self.app.transactions if trans["type"] == "Expense")
        all_categories = sorted(all_budget_categories.union(all_expense_categories))

        budget_values = [month_budgets.get(cat, 0) for cat in all_categories]
        expense_values = [category_expenses.get(cat, 0) for cat in all_categories]
        
        if all(v == 0 for v in budget_values) and all(v == 0 for v in expense_values):
            CTkLabel(self.budget_vs_actual_tab, text="No budget or expense data for this month.", font=("Arial", 14), text_color = 'gray').pack(pady=20)
            return
        
        fig = Figure(figsize=(8, 4))
        ax = fig.add_subplot(111)

        bar_width = 0.35
        x = range(len(all_categories))

        ax.bar([i - bar_width/2 for i in x], budget_values, width=bar_width, label='Budget', color='#2a9d8f')
        ax.bar([i + bar_width/2 for i in x], expense_values, width=bar_width, label='Actual Expense', color='#e76f51')

        ax.set_xlabel('Category', fontsize = 14)
        ax.set_ylabel('Amount ($)', fontsize = 14)
        ax.set_title(f"Budget vs Actual Expense - {datetime(self.app.current_year, self.app.current_month, 1).strftime('%B %Y')}", fontsize = 16)
        ax.set_xticks(x)
        ax.set_xticklabels(all_categories, fontsize = 12)
        ax.legend(fontsize = 12)
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.budget_vs_actual_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

