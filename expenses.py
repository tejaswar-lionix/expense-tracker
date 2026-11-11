#!/usr/bin/env python3
"""Track expenses in a JSON file and summarise spending by category."""
import json
import os
from datetime import date

DEFAULT_PATH = os.path.expanduser("~/.expenses.json")
CATEGORIES = ("food", "transport", "home", "fun", "other")


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save(path, expenses):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(expenses, handle, indent=2)


def add_expense(expenses, amount, category, note="", day=None):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if category not in CATEGORIES:
        raise ValueError(f"unknown category: {category}")
    expenses.append(
        {
            "amount": round(float(amount), 2),
            "category": category,
            "note": note,
            "date": day or date.today().isoformat(),
        }
    )
    return expenses


def total(expenses):
    return round(sum(item["amount"] for item in expenses), 2)


def by_category(expenses):
    totals = {}
    for item in expenses:
        totals[item["category"]] = round(
            totals.get(item["category"], 0) + item["amount"], 2
        )
    return totals


def monthly(expenses, month):
    """Return expenses whose date starts with month in YYYY-MM form."""
    if len(month) != 7 or month[4] != "-":
        raise ValueError("month must be formatted as YYYY-MM")
    return [item for item in expenses if item["date"].startswith(month)]
