"""Accurate equal-split calculations using integer cents."""

def calculate_split(total, number_of_people):
    if number_of_people <= 0: raise ValueError("Add at least one household member first.")
    return round(float(total) / number_of_people, 2)

def calculate_balances(paid_rows, total=None):
    """Return (name, paid, assigned_share, balance); balances sum to zero to the cent."""
    rows=list(paid_rows)
    if not rows: return []
    if total is None: total=sum(float(r["paid"]) for r in rows)
    total_cents=round(float(total)*100)
    base,remainder=divmod(total_cents,len(rows))
    result=[]
    for index,row in enumerate(rows):
        share_cents=base+(1 if index < remainder else 0)
        paid_cents=round(float(row["paid"])*100)
        result.append((row["name"],paid_cents/100,share_cents/100,(paid_cents-share_cents)/100))
    return result
