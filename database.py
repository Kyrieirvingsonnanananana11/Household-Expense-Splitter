"""SQLite data layer for Household Expense Splitter."""
import os
import sqlite3
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "expense_splitter.db")
DEFAULT_CATEGORIES = ["Food", "Electricity", "Rent", "Transport", "Groceries", "Healthcare", "Education", "Other"]

class Database:
    def __init__(self, path=DB_FILE):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()
        self._migrate_member_uniqueness()

    def _create_tables(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS user_account (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL COLLATE NOCASE UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS member (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            owner_user_id INTEGER REFERENCES user_account(user_id)
        );
        CREATE TABLE IF NOT EXISTS expense (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            expense_date TEXT NOT NULL DEFAULT (date('now')),
            category_id INTEGER NOT NULL REFERENCES category(category_id),
            paid_by INTEGER NOT NULL REFERENCES member(member_id),
            owner_user_id INTEGER REFERENCES user_account(user_id)
        );
        """)
        member_cols = {r[1] for r in self.conn.execute("PRAGMA table_info(member)")}
        expense_cols = {r[1] for r in self.conn.execute("PRAGMA table_info(expense)")}
        if "owner_user_id" not in member_cols:
            self.conn.execute("ALTER TABLE member ADD COLUMN owner_user_id INTEGER REFERENCES user_account(user_id)")
        if "owner_user_id" not in expense_cols:
            self.conn.execute("ALTER TABLE expense ADD COLUMN owner_user_id INTEGER REFERENCES user_account(user_id)")
        for category in DEFAULT_CATEGORIES:
            self.conn.execute("INSERT OR IGNORE INTO category(category_name) VALUES (?)", (category,))
        self.conn.commit()

    def _migrate_member_uniqueness(self):
        """Replace the old global UNIQUE(name) rule with per-account uniqueness."""
        indexes = self.conn.execute("PRAGMA index_list(member)").fetchall()
        has_global_unique = False
        for index in indexes:
            if index[2]:
                cols = [r[2] for r in self.conn.execute(f"PRAGMA index_info('{index[1]}')")]
                if cols == ["name"]:
                    has_global_unique = True
        if not has_global_unique:
            return
        self.conn.commit()
        self.conn.execute("PRAGMA foreign_keys = OFF")
        try:
            self.conn.execute("BEGIN")
            self.conn.execute("""CREATE TABLE member_new (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner_user_id INTEGER REFERENCES user_account(user_id),
                UNIQUE(owner_user_id, name)
            )""")
            self.conn.execute("INSERT INTO member_new(member_id,name,owner_user_id) SELECT member_id,name,owner_user_id FROM member")
            self.conn.execute("DROP TABLE member")
            self.conn.execute("ALTER TABLE member_new RENAME TO member")
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            self.conn.execute("PRAGMA foreign_keys = ON")

    def create_user(self, username, password_hash, salt):
        cur = self.conn.execute("INSERT INTO user_account(username,password_hash,salt) VALUES(?,?,?)", (username,password_hash,salt))
        user_id = cur.lastrowid
        if self.conn.execute("SELECT COUNT(*) FROM user_account").fetchone()[0] == 1:
            self.conn.execute("UPDATE member SET owner_user_id=? WHERE owner_user_id IS NULL", (user_id,))
            self.conn.execute("UPDATE expense SET owner_user_id=? WHERE owner_user_id IS NULL", (user_id,))
        self.conn.commit()
        return user_id

    def get_user(self, username):
        return self.conn.execute("SELECT * FROM user_account WHERE username=? COLLATE NOCASE", (username,)).fetchone()

    def get_members(self, user_id):
        return self.conn.execute("SELECT member_id,name FROM member WHERE owner_user_id=? ORDER BY name COLLATE NOCASE", (user_id,)).fetchall()

    def add_member(self, user_id, name):
        cur=self.conn.execute("INSERT INTO member(name,owner_user_id) VALUES(?,?)", (name,user_id)); self.conn.commit(); return cur.lastrowid

    def delete_member(self, user_id, member_id):
        self.conn.execute("DELETE FROM member WHERE member_id=? AND owner_user_id=?", (member_id,user_id)); self.conn.commit()

    def get_categories(self):
        return self.conn.execute("SELECT category_id,category_name FROM category ORDER BY category_name").fetchall()

    def add_expense(self, user_id, description, amount, category_id, paid_by, expense_date=None):
        self.conn.execute("INSERT INTO expense(description,amount,expense_date,category_id,paid_by,owner_user_id) VALUES(?,?,?,?,?,?)",
            (description,amount,expense_date or date.today().isoformat(),category_id,paid_by,user_id)); self.conn.commit()

    def update_expense(self, user_id, expense_id, description, amount, category_id, paid_by, expense_date):
        self.conn.execute("UPDATE expense SET description=?,amount=?,category_id=?,paid_by=?,expense_date=? WHERE expense_id=? AND owner_user_id=?",
            (description,amount,category_id,paid_by,expense_date,expense_id,user_id)); self.conn.commit()

    def delete_expense(self, user_id, expense_id):
        self.conn.execute("DELETE FROM expense WHERE expense_id=? AND owner_user_id=?", (expense_id,user_id)); self.conn.commit()

    def delete_all_expenses(self, user_id):
        self.conn.execute("DELETE FROM expense WHERE owner_user_id=?", (user_id,)); self.conn.commit()

    def get_expenses(self, user_id, search="", category="All", date_from="", date_to=""):
        sql = """SELECT e.expense_id,e.description,e.expense_date,c.category_name,e.amount,m.name,e.category_id,e.paid_by
                 FROM expense e JOIN category c ON c.category_id=e.category_id
                 JOIN member m ON m.member_id=e.paid_by WHERE e.owner_user_id=?"""
        args=[user_id]
        if search.strip(): sql += " AND (e.description LIKE ? OR m.name LIKE ?)"; args.extend([f"%{search.strip()}%",f"%{search.strip()}%"])
        if category and category != "All": sql += " AND c.category_name=?"; args.append(category)
        if date_from: sql += " AND e.expense_date>=?"; args.append(date_from)
        if date_to: sql += " AND e.expense_date<=?"; args.append(date_to)
        sql += " ORDER BY e.expense_date DESC,e.expense_id DESC"
        return self.conn.execute(sql,args).fetchall()

    def get_expense(self, user_id, expense_id):
        return self.conn.execute("SELECT description,amount,category_id,paid_by,expense_date FROM expense WHERE expense_id=? AND owner_user_id=?", (expense_id,user_id)).fetchone()

    def total_expense(self, user_id):
        return self.conn.execute("SELECT COALESCE(SUM(amount),0) FROM expense WHERE owner_user_id=?",(user_id,)).fetchone()[0]

    def expense_count(self, user_id):
        return self.conn.execute("SELECT COUNT(*) FROM expense WHERE owner_user_id=?",(user_id,)).fetchone()[0]

    def paid_per_member(self, user_id):
        return self.conn.execute("""SELECT m.member_id,m.name,COALESCE(SUM(e.amount),0) AS paid
            FROM member m LEFT JOIN expense e ON e.paid_by=m.member_id AND e.owner_user_id=?
            WHERE m.owner_user_id=? GROUP BY m.member_id ORDER BY m.name COLLATE NOCASE""",(user_id,user_id)).fetchall()

    def category_totals(self, user_id):
        return self.conn.execute("""SELECT c.category_name, SUM(e.amount) AS total FROM expense e
            JOIN category c ON c.category_id=e.category_id WHERE e.owner_user_id=?
            GROUP BY c.category_id ORDER BY total DESC""",(user_id,)).fetchall()

    def recent_expenses(self, user_id, limit=6):
        return self.conn.execute("""SELECT e.expense_date,e.description,e.amount,c.category_name,m.name
            FROM expense e JOIN category c ON c.category_id=e.category_id JOIN member m ON m.member_id=e.paid_by
            WHERE e.owner_user_id=? ORDER BY e.expense_date DESC,e.expense_id DESC LIMIT ?""",(user_id,limit)).fetchall()

    def close(self): self.conn.close()
