
import json


def save_tournament(teams: list, fixtures: list, filename: str) -> None:
    """Save tournament teams and fixtures to a JSON file."""

    tournament_data = {
        "version": 1,
        "teams": teams,
        "fixtures": fixtures
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tournament_data, file, indent=4)


def load_tournament(filename: str) -> dict:
    """Load and validate tournament data from a JSON file."""

    with open(filename, "r", encoding="utf-8") as file:
        tournament_data = json.load(file)

    # Ensure the loaded data is a dictionary.
    if not isinstance(tournament_data, dict):
        raise ValueError("Invalid tournament file format.")

    # Check required top-level keys.
    required_keys = {"version", "teams", "fixtures"}

    if not required_keys.issubset(tournament_data):
        raise ValueError("Tournament file is missing required information.")

    # Check the file version.
    if type(tournament_data["version"]) is not int or tournament_data["version"] != 1:
        raise ValueError("Unsupported tournament file version.")

    teams = tournament_data["teams"]
    fixtures = tournament_data["fixtures"]

    # Ensure teams and fixtures are lists.
    if not isinstance(teams, list):
        raise ValueError("Teams data must be a list.")

    if not isinstance(fixtures, list):
        raise ValueError("Fixtures data must be a list.")

    # A tournament must contain between 4 and 8 teams.
    if not 4 <= len(teams) <= 8:
        raise ValueError("A tournament must have between 4 and 8 teams.")

    # Track team IDs and names.
    team_ids = set()
    team_names = set()

    # Validate every team.
    for team in teams:

        if not isinstance(team, dict):
            raise ValueError("Each team must be a dictionary.")

        if "id" not in team or "name" not in team:
            raise ValueError("Each team must have an ID and a name.")

        team_id = team["id"]
        team_name = team["name"]

        if not isinstance(team_id, str) or not team_id.strip():
            raise ValueError("Each team must have a valid ID.")

        if not isinstance(team_name, str):
            raise ValueError("Team names must be text.")

        team_name = team_name.strip()

        if not 2 <= len(team_name) <= 30:
            raise ValueError("Team names must be between 2 and 30 characters.")

        if team_id in team_ids:
            raise ValueError("Duplicate team ID found.")

        if team_name.casefold() in team_names:
            raise ValueError("Duplicate team name found.")

        team_ids.add(team_id)
        team_names.add(team_name.casefold())

    # Calculate the expected number of fixtures.
    expected_fixture_count = len(teams) * (len(teams) - 1) // 2

    if len(fixtures) != expected_fixture_count:
        raise ValueError("Incorrect number of fixtures.")

    # Track fixture IDs and team pairings.
    fixture_ids = set()
    match_pairs = set()

    # Validate every fixture.
    for number, fixture in enumerate(fixtures, start=1):

        if not isinstance(fixture, dict):
            raise ValueError("Each fixture must be a dictionary.")

        required_fixture_keys = {
            "id",
            "home_team_id",
            "away_team_id",
            "status"
        }

        if not required_fixture_keys.issubset(fixture):
            raise ValueError("Fixture is missing required information.")

        fixture_id = fixture["id"]
        home_team_id = fixture["home_team_id"]
        away_team_id = fixture["away_team_id"]
        status = fixture["status"]

        # Check fixture ID format and sequence.
        expected_id = f"M{number:03d}"

        if fixture_id != expected_id:
            raise ValueError("Invalid fixture ID or sequence.")

        # Check that fixture IDs are unique.
        if fixture_id in fixture_ids:
            raise ValueError("Duplicate fixture ID found.")

        fixture_ids.add(fixture_id)

        # Check that both teams exist.
        if home_team_id not in team_ids or away_team_id not in team_ids:
            raise ValueError("Fixture references an unknown team.")

        # A team cannot play against itself.
        if home_team_id == away_team_id:
            raise ValueError("A team cannot play against itself.")

        # Check that the pairing has not already appeared.
        pairing = frozenset([home_team_id, away_team_id])

        if pairing in match_pairs:
            raise ValueError("Duplicate fixture pairing found.")

        match_pairs.add(pairing)

        # Only pending and played statuses are allowed.
        if status not in ["pending", "played"]:
            raise ValueError("Invalid fixture status.")

        # Pending fixtures must not have scores.
        if status == "pending":
            if "home_score" in fixture or "away_score" in fixture:
                raise ValueError("Pending fixtures cannot have scores.")

        # Played fixtures must have two valid scores.
        if status == "played":

            if "home_score" not in fixture or "away_score" not in fixture:
                raise ValueError("Played fixtures must have both scores.")

            home_score = fixture["home_score"]
            away_score = fixture["away_score"]

            if type(home_score) is not int or type(away_score) is not int:
                raise ValueError("Scores must be whole numbers.")

            if home_score < 0 or away_score < 0:
                raise ValueError("Scores cannot be negative.")

    return tournament_data
