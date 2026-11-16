
MIN_TEAMS = 4
MAX_TEAMS = 8
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 30


def register_team(teams: list, name: str) -> dict:
    """Register a team and return its information."""

    # Check that the team name is a string.
    if not isinstance(name, str):
        raise ValueError("Team name must be text.")

    # Remove unnecessary spaces around the name.
    name = name.strip()

    # Check the length of the team name.
    if len(name) < MIN_NAME_LENGTH or len(name) > MAX_NAME_LENGTH:
        raise ValueError("Team name must be between 2 and 30 characters.")

    # Prevent duplicate team names.
    for team in teams:
        if team["name"].casefold() == name.casefold():
            raise ValueError("This team has already been registered.")

    # Prevent registration beyond the maximum limit.
    if len(teams) >= MAX_TEAMS:
        raise ValueError("A tournament cannot have more than 8 teams.")

    # Generate a unique team ID.
    team_id = f"TM{len(teams) + 1:03d}"

    # Create the team record.
    new_team = {
        "id": team_id,
        "name": name
    }

    # Add the team to the list.
    teams.append(new_team)

    return new_team


def validate_team_count(teams: list) -> bool:
    """Check whether the tournament has between 4 and 8 teams."""

    if len(teams) < MIN_TEAMS or len(teams) > MAX_TEAMS:
        raise ValueError("A tournament must have between 4 and 8 teams.")

    return True
