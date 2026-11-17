import json
import os
import tempfile
import unittest

from tournament.teams import register_team
from tournament.fixtures import generate_fixtures
from tournament.storage import save_tournament, load_tournament


class TestTournamentStorage(unittest.TestCase):

    def setUp(self):
        self.teams = []

        for name in ["Thunder", "Comets", "Phoenix", "Rockets"]:
            register_team(self.teams, name)

        self.fixtures = generate_fixtures(self.teams)

    def test_save_and_load_tournament(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "tournament.json")

            save_tournament(self.teams, self.fixtures, filename)
            loaded_data = load_tournament(filename)

            self.assertEqual(loaded_data["teams"], self.teams)
            self.assertEqual(loaded_data["fixtures"], self.fixtures)
            self.assertEqual(loaded_data["version"], 1)

    def test_invalid_fixture_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "invalid.json")

            data = {
                "version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            data["fixtures"][0]["status"] = "cancelled"

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file)

            with self.assertRaisesRegex(ValueError, "Invalid fixture status"):
                load_tournament(filename)

    def test_pending_fixture_with_score_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "invalid.json")

            data = {
                "version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            data["fixtures"][0]["home_score"] = 2

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file)

            with self.assertRaisesRegex(ValueError, "Pending fixtures cannot have scores"):
                load_tournament(filename)

    def test_played_fixture_without_both_scores_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "invalid.json")

            data = {
                "version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            data["fixtures"][0]["status"] = "played"
            data["fixtures"][0]["home_score"] = 2

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file)

            with self.assertRaisesRegex(ValueError, "Played fixtures must have both scores"):
                load_tournament(filename)

    def test_negative_score_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "invalid.json")

            data = {
                "version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            data["fixtures"][0]["status"] = "played"
            data["fixtures"][0]["home_score"] = -1
            data["fixtures"][0]["away_score"] = 2

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file)

            with self.assertRaisesRegex(ValueError, "Scores cannot be negative"):
                load_tournament(filename)

    def test_boolean_score_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "invalid.json")

            data = {
                "version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            data["fixtures"][0]["status"] = "played"
            data["fixtures"][0]["home_score"] = True
            data["fixtures"][0]["away_score"] = 2

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file)

            with self.assertRaisesRegex(ValueError, "Scores must be whole numbers"):
                load_tournament(filename)


if __name__ == "__main__":
    unittest.main()
