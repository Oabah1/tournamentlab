
import unittest

from tournament.teams import register_team
from tournament.fixtures import generate_fixtures


class TestFixtureGeneration(unittest.TestCase):

    def setUp(self):
        self.teams = []

        for name in ["Thunder", "Comets", "Phoenix", "Rockets"]:
            register_team(self.teams, name)

    def test_six_fixtures_are_generated_for_four_teams(self):
        fixtures = generate_fixtures(self.teams)

        self.assertEqual(len(fixtures), 6)

    def test_fixture_ids_are_generated_correctly(self):
        fixtures = generate_fixtures(self.teams)

        expected_ids = [
            "M001", "M002", "M003",
            "M004", "M005", "M006"
        ]

        actual_ids = [fixture["id"] for fixture in fixtures]

        self.assertEqual(actual_ids, expected_ids)

    def test_every_fixture_has_two_different_teams(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertNotEqual(
                fixture["home_team_id"],
                fixture["away_team_id"]
            )

    def test_no_team_pairing_is_repeated(self):
        fixtures = generate_fixtures(self.teams)

        pairings = []

        for fixture in fixtures:
            pairing = frozenset([
                fixture["home_team_id"],
                fixture["away_team_id"]
            ])

            pairings.append(pairing)

        self.assertEqual(len(pairings), len(set(pairings)))

    def test_all_fixtures_start_as_pending(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertEqual(fixture["status"], "pending")

    def test_three_teams_cannot_generate_fixtures(self):
        small_teams = self.teams[:3]

        with self.assertRaises(ValueError):
            generate_fixtures(small_teams)

    def test_nine_teams_cannot_generate_fixtures(self):
        large_teams = [
            {"id": f"TM{number:03d}", "name": f"Team {number}"}
            for number in range(1, 10)
        ]

        with self.assertRaises(ValueError):
            generate_fixtures(large_teams)


if __name__ == "__main__":
    unittest.main()
