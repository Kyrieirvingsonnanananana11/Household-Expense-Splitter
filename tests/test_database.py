import os
import tempfile
import unittest
from database import Database
from authentication import make_password_hash

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        self.db = Database(self.path)
        digest, salt = make_password_hash("example-password")
        self.user_a = self.db.create_user("account_a", digest, salt)
        self.user_b = self.db.create_user("account_b", digest, salt)

    def tearDown(self):
        self.db.close()
        os.remove(self.path)

    def test_same_member_name_allowed_for_separate_accounts(self):
        self.db.add_member(self.user_a, "Asha")
        self.db.add_member(self.user_b, "Asha")
        self.assertEqual(len(self.db.get_members(self.user_a)), 1)
        self.assertEqual(len(self.db.get_members(self.user_b)), 1)

    def test_expenses_are_isolated_by_account(self):
        member = self.db.add_member(self.user_a, "Asha")
        category = self.db.get_categories()[0]["category_id"]
        self.db.add_expense(self.user_a, "Groceries", 250.00, category, member, "2026-11-15")
        self.assertEqual(self.db.total_expense(self.user_a), 250.00)
        self.assertEqual(self.db.total_expense(self.user_b), 0.00)
        self.assertEqual(len(self.db.get_expenses(self.user_a, date_from="2026-11-01")), 1)
        self.assertEqual(len(self.db.get_expenses(self.user_b)), 0)

if __name__ == "__main__":
    unittest.main()
