CATEGORIES = {
    "Entertainment": ["Movies", "Games", "Concerts"],
    "Food": ["Groceries", "Dining Out", "Snacks"],
    "Utilities": ["Electricity", "Water", "Internet"],
    "Others": ["Miscellaneous"]
}

def get_all_categories():
    return list(CATEGORIES.keys())

def get_subcategories(category):
    return CATEGORIES.get(category, [])


