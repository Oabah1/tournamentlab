
import unittest

from tournament.teams import register_team
from tournament.fixtures import generate_fixtures
from tournament.results import record_result


class TestResultRecording(unittest.TestCase):

    def setUp(self):
        teams = []

        for name in ["Thunder", "Comets", "Phoenix", "Rockets"]:
            register_team(teams, name)

        self.fixtures = generate_fixtures(teams)

    def test_valid_result_is_recorded(self):
        result = record_result(self.fixtures, "M001", 3, 1)

        self.assertEqual(result["home_score"], 3)
        self.assertEqual(result["away_score"], 1)

    def test_fixture_status_changes_to_played(self):
        result = record_result(self.fixtures, "M001", 2, 0)

        self.assertEqual(result["status"], "played")

    def test_unknown_fixture_id_is_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M999", 2, 1)

    def test_duplicate_result_is_rejected(self):
        record_result(self.fixtures, "M001", 2, 1)

        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", 3, 0)

    def test_negative_scores_are_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", -1, 2)

        self.assertEqual(self.fixtures[0]["status"], "pending")

    def test_decimal_scores_are_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", 2.5, 1)

        self.assertEqual(self.fixtures[0]["status"], "pending")

    def test_text_scores_are_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", "two", 1)

        self.assertEqual(self.fixtures[0]["status"], "pending")

    def test_boolean_scores_are_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", True, 1)

        self.assertEqual(self.fixtures[0]["status"], "pending")

    def test_zero_scores_are_allowed(self):
        result = record_result(self.fixtures, "M001", 0, 0)

        self.assertEqual(result["home_score"], 0)
        self.assertEqual(result["away_score"], 0)
        self.assertEqual(result["status"], "played")


if __name__ == "__main__":
    unittest.main()
