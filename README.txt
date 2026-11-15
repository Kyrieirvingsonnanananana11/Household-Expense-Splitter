HOMEWISE — HOUSEHOLD EXPENSE SPLITTER
====================================

WHAT IS INCLUDED
- Individual local accounts with password hashing.
- Dashboard with household totals, recent activity, and category breakdown.
- Household member management.
- Add and edit expenses, including the expense date.
- Search by description or member, filter by category and date range.
- Delete selected expenses and export the filtered history to CSV.
- Equal split summary with cent-level rounding so member balances total zero.
- Separate Python files for each page and reusable database, validation, calculation, and UI modules.

REQUIREMENTS
- Python 3.10 or newer (tested for syntax with Python 3.13).
- Tkinter (included with most Windows Python installations).
- No third-party packages are required.

RUN IN VS CODE
1. Open this folder in VS Code.
2. Choose Terminal > New Terminal.
3. Run: py main.py
   If that command is unavailable, run: python main.py

FIRST USE
1. Create an account and sign in.
2. Add household members.
3. Add expenses and choose the member who paid.
4. Review the dashboard and split summary.
5. Open Expense history to search, filter, edit, delete, or export records.

PROJECT STRUCTURE
main.py                  Main window, navigation, and application shell
ui.py                    Shared colours, ttk styles, and UI helpers
database.py              SQLite database, queries, and schema migration
authentication.py        Password hashing and verification
validators.py             Reusable input validation
calculations.py           Equal split and balance calculations
pages/login.py            Login page
pages/register.py         Registration page
pages/dashboard.py        Dashboard and category overview
pages/members.py          Household member management
pages/add_expense.py      Add/edit expense form
pages/expense_history.py  Search, filters, edit/delete, CSV export
pages/split_summary.py    Per-member settlement summary

DATA AND BACKUP
- The app creates expense_splitter.db in this folder automatically.
- Back up expense_splitter.db before replacing an older project version.
- Existing unassigned records from the previous single-user version are assigned to the first account registered after migration.
- The member table is upgraded to allow the same member name in different accounts.
- Each account's household members and expenses are filtered by its account ID.

PROJECT SCOPE AND LIMITATIONS
- This is a local educational desktop application, not an online banking service.
- No cloud sync, online payments, bank/e-wallet connection, or password reset.
- Expenses are split equally among all household members; custom/unequal splits are not included.
- CSV export contains the currently filtered records only.
- Passwords are hashed locally, but this project is not intended as production-grade account security.

RUN THE BUILT-IN TESTS
From the project folder, run:
    py -m unittest discover -s tests -v
The tests check split rounding, account separation, and basic database behavior.
