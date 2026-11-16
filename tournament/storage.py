
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
    """Load tournament data from a JSON file."""

    with open(filename, "r", encoding="utf-8") as file:
        tournament_data = json.load(file)

    # Ensure the loaded data is a dictionary.
    if not isinstance(tournament_data, dict):
        raise ValueError("Invalid tournament file format.")

    # Check that all required keys are present.
    required_keys = {"version", "teams", "fixtures"}

    if not required_keys.issubset(tournament_data):
        raise ValueError("Tournament file is missing required information.")

    # Check that the file uses a supported version.
    if tournament_data.get("version") != 1:
        raise ValueError("Unsupported tournament file version.")

    # Ensure teams and fixtures are lists.
    if not isinstance(tournament_data["teams"], list):
        raise ValueError("Teams data must be a list.")

    if not isinstance(tournament_data["fixtures"], list):
        raise ValueError("Fixtures data must be a list.")

    # Ensure the tournament has between 4 and 8 teams.
    if len(tournament_data["teams"]) < 4 or len(tournament_data["teams"]) > 8:
        raise ValueError("A tournament must have between 4 and 8 teams.")

    # Track team IDs and names to prevent duplicates.
    team_ids = set()
    team_names = set()

    # Validate every team record.
    for team in tournament_data["teams"]:

        if not isinstance(team, dict):
            raise ValueError("Each team must be a dictionary.")

        if "id" not in team or "name" not in team:
            raise ValueError("Each team must have an ID and a name.")

        team_id = team["id"]
        team_name = team["name"]

        # Check that the team ID is valid.
        if not isinstance(team_id, str) or not team_id.strip():
            raise ValueError("Each team must have a valid ID.")

        # Check that the team name is text.
        if not isinstance(team_name, str):
            raise ValueError("Team names must be text.")

        team_name = team_name.strip()

        # Check that the team name is not empty.
        if not team_name:
            raise ValueError("Team names cannot be empty.")

        # Check the team name length.
        if len(team_name) < 2 or len(team_name) > 30:
            raise ValueError("Team names must be between 2 and 30 characters.")

        # Reject duplicate team IDs.
        if team_id in team_ids:
            raise ValueError("Duplicate team ID found.")

        # Reject duplicate team names, ignoring letter case.
        if team_name.casefold() in team_names:
            raise ValueError("Duplicate team name found.")

        team_ids.add(team_id)
        team_names.add(team_name.casefold())

    return tournament_data
