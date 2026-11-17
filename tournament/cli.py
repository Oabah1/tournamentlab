from tournament.teams import register_team
from tournament.fixtures import generate_fixtures
from tournament.results import record_result
from tournament.standings import calculate_standings
from tournament.storage import save_tournament, load_tournament


def display_menu():
    """Display the TournamentLab main menu."""

    print("\n" + "=" * 40)
    print("       TOURNAMENTLAB MANAGER")
    print("=" * 40)

    print("1. Register a team")
    print("2. View registered teams")
    print("3. Generate fixtures")
    print("4. View fixtures")
    print("5. Record match result")
    print("6. View league table")
    print("7. Save tournament")
    print("8. Load tournament")
    print("9. Exit")

    print("=" * 40)


def register_team_option(teams):
    """Ask for a team name and register the team."""

    team_name = input("Enter team name: ")

    try:
        team = register_team(teams, team_name)
        print(f"Successfully registered {team['name']}!")
        print(f"Team ID: {team['id']}")

    except ValueError as error:
        print(f"Error: {error}")


def view_teams_option(teams):
    """Display all registered teams."""

    print("\nREGISTERED TEAMS")
    print("-" * 40)

    if not teams:
        print("No teams have been registered yet.")
        return

    for team in teams:
        print(f"{team['id']}  {team['name']}")

    print("-" * 40)
    print(f"Total teams: {len(teams)}")


def generate_fixtures_option(teams, fixtures):
    """Generate tournament fixtures."""

    try:
        if fixtures:
            print("Fixtures have already been generated.")
            return

        fixtures.extend(generate_fixtures(teams))
        print("\nFixtures generated successfully!")
        print(f"Total fixtures: {len(fixtures)}")

    except ValueError as error:
        print(f"Error: {error}")


def find_team_name(teams, team_id):
    """Find a team's name using its ID."""

    for team in teams:
        if team["id"] == team_id:
            return team["name"]

    return "Unknown team"


def view_fixtures_option(teams, fixtures):
    """Display all tournament fixtures."""

    print("\nTOURNAMENT FIXTURES")
    print("-" * 55)

    if not fixtures:
        print("No fixtures have been generated yet.")
        return

    for fixture in fixtures:
        home_name = find_team_name(teams, fixture["home_team_id"])
        away_name = find_team_name(teams, fixture["away_team_id"])
        status = fixture["status"].upper()

        if status == "PLAYED":
            print(
                f"{fixture['id']}  "
                f"{home_name} {fixture['home_score']} - "
                f"{fixture['away_score']} {away_name}  "
                f"[{status}]"
            )
        else:
            print(
                f"{fixture['id']}  "
                f"{home_name} vs {away_name}  "
                f"[{status}]"
            )

    print("-" * 55)
    print(f"Total fixtures: {len(fixtures)}")


def record_result_option(fixtures):
    """Ask for match scores and record the result."""

    if not fixtures:
        print("Generate fixtures before recording results.")
        return

    fixture_id = input("Enter fixture ID: ").strip()

    try:
        home_score = int(input("Enter home team score: "))
        away_score = int(input("Enter away team score: "))

        result = record_result(
            fixtures, fixture_id, home_score, away_score
        )

        print("\nMatch result recorded successfully!")
        print(
            f"Score: {result['home_score']} - "
            f"{result['away_score']}"
        )

    except ValueError as error:
        print(f"Error: {error}")


def view_standings_option(teams, fixtures):
    """Display the tournament league table."""

    if not teams:
        print("Register teams before viewing the league table.")
        return

    if not fixtures:
        print("Generate fixtures before viewing the league table.")
        return

    standings = calculate_standings(teams, fixtures)

    print("\nTOURNAMENT LEAGUE TABLE")
    print("-" * 85)

    print(
        f"{'Team':<12}"
        f"{'P':>4}"
        f"{'W':>4}"
        f"{'D':>4}"
        f"{'L':>4}"
        f"{'GF':>5}"
        f"{'GA':>5}"
        f"{'GD':>5}"
        f"{'Pts':>6}"
    )

    print("-" * 85)

    for team in standings:
        print(
            f"{team['team_name']:<12}"
            f"{team['played']:>4}"
            f"{team['won']:>4}"
            f"{team['drawn']:>4}"
            f"{team['lost']:>4}"
            f"{team['goals_for']:>5}"
            f"{team['goals_against']:>5}"
            f"{team['goal_difference']:>5}"
            f"{team['points']:>6}"
        )

    print("-" * 85)


def save_tournament_option(teams, fixtures):
    """Save tournament data to a JSON file."""

    if not teams:
        print("Register teams before saving the tournament.")
        return

    filename = input(
        "Enter filename (press Enter for data/tournament.json): "
    ).strip()

    if not filename:
        filename = "data/tournament.json"

    try:
        save_tournament(teams, fixtures, filename)
        print(f"Tournament saved successfully to {filename}!")

    except OSError as error:
        print(f"File error: {error}")


def load_tournament_option(teams, fixtures):
    """Load tournament data from a JSON file."""

    filename = input(
        "Enter filename (press Enter for data/tournament.json): "
    ).strip()

    if not filename:
        filename = "data/tournament.json"

    try:
        tournament_data = load_tournament(filename)

        teams[:] = tournament_data["teams"]
        fixtures[:] = tournament_data["fixtures"]

        print(f"Tournament loaded successfully from {filename}!")
        print(f"Teams loaded: {len(teams)}")
        print(f"Fixtures loaded: {len(fixtures)}")

    except (OSError, ValueError) as error:
        print(f"Error loading tournament: {error}")


def run_cli():
    """Start the TournamentLab command-line interface."""

    teams = []
    fixtures = []

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_team_option(teams)

        elif choice == "2":
            view_teams_option(teams)

        elif choice == "3":
            generate_fixtures_option(teams, fixtures)

        elif choice == "4":
            view_fixtures_option(teams, fixtures)

        elif choice == "5":
            record_result_option(fixtures)

        elif choice == "6":
            view_standings_option(teams, fixtures)

        elif choice == "7":
            save_tournament_option(teams, fixtures)

        elif choice == "8":
            load_tournament_option(teams, fixtures)

        elif choice == "9":
            print("Thank you for using TournamentLab!")
            break

        else:
            print("This option is not available yet.")


if __name__ == "__main__":
    run_cli()
