from datetime import datetime

def update_month_display(app):
    if hasattr(app, 'home_tab') and hasattr(app.home_tab, 'month_label'):
        app.home_tab.month_label.configure(text=f"{datetime(app.current_year, app.current_month, 1).strftime('%B %Y')}")
    if hasattr(app, 'budget_tab') and hasattr(app.budget_tab, 'month_label'):
        app.budget_tab.month_label.configure(text=f"{datetime(app.current_year, app.current_month, 1).strftime('%B %Y')}")
    if hasattr(app, 'summary_tab') and hasattr(app.summary_tab, 'month_label'):
        app.summary_tab.month_label.configure(text=f"{datetime(app.current_year, app.current_month, 1).strftime('%B %Y')}")

def change_month(app, delta):
    app.current_month += delta
    if app.current_month > 12:
        app.current_month = 1
        app.current_year += 1
    elif app.current_month < 1:
        app.current_month = 12
        app.current_year -= 1
    update_month_display(app)
    if hasattr(app, 'home_tab'):
        app.home_tab.filter_transactions_by_month()
    if hasattr(app, 'budget_tab'):
        app.budget_tab.update_budget_display()
    if hasattr(app, 'summary_tab'):
        app.summary_tab.update_summary_chart()