
from itertools import combinations

from tournament.teams import validate_team_count


def generate_fixtures(teams: list) -> list:
    """Generate a single round-robin schedule."""

    # Ensure the tournament has between 4 and 8 teams.
    validate_team_count(teams)

    fixtures = []

    # Generate every possible pair of teams.
    team_pairs = combinations(teams, 2)

    # Give each fixture a unique ID.
    for number, (team_a, team_b) in enumerate(team_pairs, start=1):

        fixture = {
            "id": f"M{number:03d}",
            "home_team_id": team_a["id"],
            "away_team_id": team_b["id"],
            "status": "pending"
        }

        fixtures.append(fixture)

    return fixtures
