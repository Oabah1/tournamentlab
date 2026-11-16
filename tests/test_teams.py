
import unittest

from tournament.teams import register_team, validate_team_count


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.teams = []

    def test_register_team_successfully(self):
        team = register_team(self.teams, "Thunder")

        self.assertEqual(team["id"], "TM001")
        self.assertEqual(team["name"], "Thunder")
        self.assertEqual(len(self.teams), 1)

    def test_team_ids_are_generated_correctly(self):
        register_team(self.teams, "Thunder")
        register_team(self.teams, "Comets")

        self.assertEqual(self.teams[0]["id"], "TM001")
        self.assertEqual(self.teams[1]["id"], "TM002")

    def test_team_name_spaces_are_removed(self):
        team = register_team(self.teams, "  Thunder  ")

        self.assertEqual(team["name"], "Thunder")

    def test_duplicate_team_names_are_rejected(self):
        register_team(self.teams, "Thunder")

        with self.assertRaises(ValueError):
            register_team(self.teams, "thunder")

        self.assertEqual(len(self.teams), 1)

    def test_non_string_team_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, 123)

    def test_short_team_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A")

    def test_long_team_name_is_rejected(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A" * 31)

    def test_ninth_team_is_rejected(self):
        names = [
            "Thunder", "Comets", "Phoenix", "Rockets",
            "Falcons", "Titans", "Warriors", "Dragons"
        ]

        for name in names:
            register_team(self.teams, name)

        with self.assertRaises(ValueError):
            register_team(self.teams, "Eagles")

        self.assertEqual(len(self.teams), 8)

    def test_four_teams_are_valid(self):
        for name in ["Thunder", "Comets", "Phoenix", "Rockets"]:
            register_team(self.teams, name)

        self.assertTrue(validate_team_count(self.teams))

    def test_three_teams_are_invalid(self):
        for name in ["Thunder", "Comets", "Phoenix"]:
            register_team(self.teams, name)

        with self.assertRaises(ValueError):
            validate_team_count(self.teams)


if __name__ == "__main__":
    unittest.main()
