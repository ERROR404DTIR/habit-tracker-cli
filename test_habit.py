import json
import os
import tempfile
import unittest
from datetime import date, timedelta

os.environ["HABITS_FILE"] = os.path.join(tempfile.mkdtemp(), "habits.json")

import habit  # noqa: E402


class StreakTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(habit.streak([]), 0)

    def test_today_and_yesterday(self):
        today = date.today()
        days = [today.isoformat(), (today - timedelta(days=1)).isoformat()]
        self.assertEqual(habit.streak(days), 2)

    def test_streak_alive_if_done_yesterday(self):
        yesterday = date.today() - timedelta(days=1)
        self.assertEqual(habit.streak([yesterday.isoformat()]), 1)

    def test_broken_streak(self):
        old = date.today() - timedelta(days=5)
        self.assertEqual(habit.streak([old.isoformat()]), 0)


class CliTests(unittest.TestCase):
    def setUp(self):
        if habit.DATA_FILE.exists():
            habit.DATA_FILE.unlink()

    def test_add_and_done(self):
        habit.main(["add", "read"])
        habit.main(["done", "read"])
        data = json.loads(habit.DATA_FILE.read_text())
        self.assertEqual(data["read"], [date.today().isoformat()])


if __name__ == "__main__":
    unittest.main()
