
def calculate_standings(teams: list, fixtures: list) -> list:
    """Calculate and return the tournament league table."""

    standings = {}

    # Create an initial record for every team.
    for team in teams:
        standings[team["id"]] = {
            "team_id": team["id"],
            "team_name": team["name"],
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

    # Process only fixtures that have been played.
    for fixture in fixtures:

        if fixture["status"] != "played":
            continue

        home = standings[fixture["home_team_id"]]
        away = standings[fixture["away_team_id"]]

        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        # Update matches played.
        home["played"] += 1
        away["played"] += 1

        # Update goals scored and conceded.
        home["goals_for"] += home_score
        home["goals_against"] += away_score

        away["goals_for"] += away_score
        away["goals_against"] += home_score

        # Award points and update match outcomes.
        if home_score > away_score:
            home["won"] += 1
            away["lost"] += 1
            home["points"] += 3

        elif home_score < away_score:
            away["won"] += 1
            home["lost"] += 1
            away["points"] += 3

        else:
            home["drawn"] += 1
            away["drawn"] += 1
            home["points"] += 1
            away["points"] += 1

    # Calculate goal difference for every team.
    for team in standings.values():
        team["goal_difference"] = (
            team["goals_for"] - team["goals_against"]
        )

    # Rank teams according to the tournament rules.
    ranked_standings = sorted(
        standings.values(),
        key=lambda team: (
            -team["points"],
            -team["goal_difference"],
            -team["goals_for"],
            team["team_name"].casefold()
        )
    )

    return ranked_standings
