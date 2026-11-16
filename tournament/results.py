
def record_result(fixtures: list, fixture_id: str, home_score: int, away_score: int) -> dict:
    """Record the result of a fixture."""

    # Find the requested fixture.
    fixture = None

    for match in fixtures:
        if match["id"] == fixture_id:
            fixture = match
            break

    # Reject an unknown fixture ID.
    if fixture is None:
        raise ValueError("Fixture not found.")

    # Prevent a fixture from receiving results twice.
    if fixture["status"] == "played":
        raise ValueError("This fixture has already been played.")

    # Ensure scores are integers, not Boolean values.
    if type(home_score) is not int or type(away_score) is not int:
        raise ValueError("Scores must be whole numbers.")

    # Reject negative scores.
    if home_score < 0 or away_score < 0:
        raise ValueError("Scores cannot be negative.")

    # Save the scores.
    fixture["home_score"] = home_score
    fixture["away_score"] = away_score

    # Update the fixture status.
    fixture["status"] = "played"

    return fixture
