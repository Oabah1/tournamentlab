
import unittest

from tournament.teams import register_team
from tournament.fixtures import generate_fixtures
from tournament.results import record_result
from tournament.standings import calculate_standings


class TestStandings(unittest.TestCase):

    def setUp(self):
        self.teams = []

        for name in ["Thunder", "Comets", "Phoenix", "Rockets"]:
            register_team(self.teams, name)

        self.fixtures = generate_fixtures(self.teams)

    def test_all_teams_appear_in_standings(self):
        table = calculate_standings(self.teams, self.fixtures)

        self.assertEqual(len(table), 4)

    def test_pending_fixtures_are_not_counted(self):
        table = calculate_standings(self.teams, self.fixtures)

        for team in table:
            self.assertEqual(team["played"], 0)

    def test_win_awards_three_points(self):
        record_result(self.fixtures, "M001", 3, 1)

        table = calculate_standings(self.teams, self.fixtures)
        thunder = next(team for team in table if team["team_name"] == "Thunder")

        self.assertEqual(thunder["points"], 3)
        self.assertEqual(thunder["won"], 1)

    def test_draw_awards_one_point_to_each_team(self):
        record_result(self.fixtures, "M001", 2, 2)

        table = calculate_standings(self.teams, self.fixtures)

        for team in table:
            if team["team_name"] in ["Thunder", "Comets"]:
                self.assertEqual(team["points"], 1)
                self.assertEqual(team["drawn"], 1)

    def test_loss_awards_zero_points(self):
        record_result(self.fixtures, "M001", 3, 1)

        table = calculate_standings(self.teams, self.fixtures)
        comets = next(team for team in table if team["team_name"] == "Comets")

        self.assertEqual(comets["points"], 0)
        self.assertEqual(comets["lost"], 1)

    def test_goals_for_and_against_are_calculated(self):
        record_result(self.fixtures, "M001", 3, 1)

        table = calculate_standings(self.teams, self.fixtures)

        thunder = next(team for team in table if team["team_name"] == "Thunder")
        comets = next(team for team in table if team["team_name"] == "Comets")

        self.assertEqual(thunder["goals_for"], 3)
        self.assertEqual(thunder["goals_against"], 1)
        self.assertEqual(comets["goals_for"], 1)
        self.assertEqual(comets["goals_against"], 3)

    def test_goal_difference_is_calculated(self):
        record_result(self.fixtures, "M001", 4, 1)

        table = calculate_standings(self.teams, self.fixtures)
        thunder = next(team for team in table if team["team_name"] == "Thunder")

        self.assertEqual(thunder["goal_difference"], 3)

    def test_higher_points_rank_first(self):
        record_result(self.fixtures, "M001", 3, 0)

        table = calculate_standings(self.teams, self.fixtures)

        self.assertEqual(table[0]["team_name"], "Thunder")

    def test_goal_difference_breaks_points_tie(self):
        record_result(self.fixtures, "M001", 3, 0)
        record_result(self.fixtures, "M002", 0, 1)

        table = calculate_standings(self.teams, self.fixtures)

        self.assertEqual(table[0]["team_name"], "Thunder")
        self.assertEqual(table[1]["team_name"], "Phoenix")

    def test_goals_for_breaks_points_and_goal_difference_tie(self):
        record_result(self.fixtures, "M001", 2, 0)
        record_result(self.fixtures, "M002", 0, 1)

        table = calculate_standings(self.teams, self.fixtures)

        self.assertEqual(table[0]["team_name"], "Thunder")
        self.assertEqual(table[1]["team_name"], "Phoenix")

    def test_team_name_breaks_complete_tie(self):
        record_result(self.fixtures, "M001", 0, 0)
        record_result(self.fixtures, "M002", 0, 0)
        record_result(self.fixtures, "M004", 0, 0)

        table = calculate_standings(self.teams, self.fixtures)

        self.assertEqual(table[0]["team_name"], "Comets")
        self.assertEqual(table[1]["team_name"], "Phoenix")
        self.assertEqual(table[2]["team_name"], "Thunder")


if __name__ == "__main__":
    unittest.main()
