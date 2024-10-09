import nfl_data_py as nfl
import pandas as pd

def fetch_weekly_data(years, team_abbr):
    """
    Fetches weekly data for the given years and filters it by the team abbreviation.
    """
    weekly_data = nfl.import_weekly_data(years)

    print("Columns in weekly_data:", weekly_data.columns)
    team_data = weekly_data[weekly_data['recent_team'] == team_abbr]

    return team_data

def main():
    years = [2022]
    team_abbr = 'KC'

    print(f"Fetching weekly data for {team_abbr}")

    # Fetch the data
    team_weekly_data = fetch_weekly_data(years, team_abbr)

    print(f"Weekly data for {team_abbr}:\n", team_weekly_data.head())

if __name__ == "__main__":
    main()
