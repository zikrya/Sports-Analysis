import nfl_data_py as nfl
import pandas as pd

def fetch_weekly_data(years, team_abbr):
    """
    Fetches weekly data for the given years and filters it by the team abbreviation.
    """
    weekly_data = nfl.import_weekly_data(years)

    relevant_columns = [
        'player_id', 'player_name', 'recent_team', 'position', 'week', 'opponent_team',
        'completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions',
        'carries', 'rushing_yards', 'rushing_tds', 'receptions', 'receiving_yards',
        'receiving_tds', 'fantasy_points', 'passing_epa', 'rushing_epa', 'receiving_epa',
        'target_share', 'air_yards_share', 'wopr'
    ]

    weekly_data = weekly_data[relevant_columns]

    print(f"Fetched data columns for {team_abbr}: {weekly_data.columns}")
    team_data = weekly_data[weekly_data['recent_team'] == team_abbr]

    return team_data

def combine_team_data(team1_data, team2_data):
    """
    Combines data from two teams into one DataFrame.
    """
    combined_data = pd.concat([team1_data, team2_data], ignore_index=True)
    return combined_data

def save_to_csv(data, filename):
    """
    Saves the filtered team data to a CSV file.
    """
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    years = [2022, 2021, 2020]
    team1_abbr = 'ATL'
    team2_abbr = 'PHI'

    print(f"Fetching weekly data for {team1_abbr} and {team2_abbr}")

    team1_data = fetch_weekly_data(years, team1_abbr)
    team2_data = fetch_weekly_data(years, team2_abbr)

    combined_data = combine_team_data(team1_data, team2_data)

    print(f"Combined data for {team1_abbr} and {team2_abbr}:\n", combined_data.head())

    # Save to a CSV file
    save_to_csv(combined_data, f'{team1_abbr}_{team2_abbr}_combined_weekly_data.csv')

if __name__ == "__main__":
    main()
