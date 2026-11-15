"""Reusable input validation."""
from datetime import date
MAX_AMOUNT = 10_000_000

def validate_username(value):
    value=value.strip()
    if len(value)<3 or len(value)>30: raise ValueError("Username must be between 3 and 30 characters.")
    if not value.replace("_","").isalnum(): raise ValueError("Use only letters, numbers and underscores in the username.")
    return value

def validate_password(value):
    if len(value)<8: raise ValueError("Password must contain at least 8 characters.")
    return value

def validate_member_name(value):
    value=value.strip()
    if not value: raise ValueError("Member name cannot be empty.")
    if len(value)>40: raise ValueError("Member name must be 40 characters or fewer.")
    return value

def validate_description(value):
    value=value.strip()
    if not value: raise ValueError("Description cannot be empty.")
    if len(value)>80: raise ValueError("Description must be 80 characters or fewer.")
    return value

def validate_amount(value):
    try: amount=float(value.strip().replace(",",""))
    except (ValueError,AttributeError): raise ValueError("Enter a valid amount, such as 1200 or 350.50.")
    if not (0<amount<=MAX_AMOUNT): raise ValueError(f"Amount must be greater than 0 and no more than Nu. {MAX_AMOUNT:,}.")
    return round(amount,2)

def validate_date(value):
    value=value.strip()
    try: parsed=date.fromisoformat(value)
    except ValueError: raise ValueError("Enter a valid date in YYYY-MM-DD format, for example 2026-11-15.")
    if parsed.isoformat()!=value: raise ValueError("Use the date format YYYY-MM-DD.")
    return value
