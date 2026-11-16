#!/usr/bin/env python3
"""Track expenses in a JSON file and summarise spending by category."""
import csv
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


def export_csv(expenses, path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["amount", "category", "note", "date"])
        for item in expenses:
            writer.writerow(
                [
                    item["amount"],
                    item["category"],
                    item.get("note", ""),
                    item["date"],
                ]
            )
    return path


def import_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        expenses = []
        for row in reader:
            expenses = add_expense(
                expenses,
                float(row["amount"]),
                row["category"],
                row.get("note") or "",
                row["date"],
            )
    return expenses


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


def set_budget(budgets, category, amount):
    """Store a monthly budget for category in the budgets mapping."""
    if category not in CATEGORIES:
        raise ValueError(f"unknown category: {category}")
    if amount < 0:
        raise ValueError("budget must not be negative")
    budgets[category] = round(float(amount), 2)
    return budgets


def budget_report(expenses, budgets, month):
    """Compare spending for month against each category budget."""
    spent = by_category(monthly(expenses, month))
    report = {}
    for category, budget in budgets.items():
        used = spent.get(category, 0.0)
        remaining = round(budget - used, 2)
        report[category] = {
            "budget": round(float(budget), 2),
            "spent": used,
            "remaining": remaining,
            "over": used > budget,
        }
    return report


def budget_warnings(expenses, budgets, month):
    """Return one message per category that has exceeded its budget."""
    warnings = []
    for category, status in budget_report(expenses, budgets, month).items():
        if status["over"]:
            over_by = round(status["spent"] - status["budget"], 2)
            warnings.append(f"{category} is over budget by {over_by:.2f}")
    return warnings
