from datetime import date
FINE_RATE = 0.50
def calculate_fine(due_date, current_date=None):
    if current_date is None:
        current_date = date.today()

    due = date.fromisoformat(due_date)
    days_late = (current_date - due).days

    return round(max(0, days_late) * FINE_RATE, 2)