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

def derive_game_result(team1_data, team2_data):
    """
    Derives game result by comparing fantasy points between two teams for each week.
    """
    results = []

    # Group both datasets by week to sum the fantasy points for the whole team
    team1_weekly = team1_data.groupby('week')['fantasy_points'].sum()
    team2_weekly = team2_data.groupby('week')['fantasy_points'].sum()

    # Find the common weeks both teams played
    common_weeks = team1_weekly.index.intersection(team2_weekly.index)

    for week in common_weeks:
        team1_fp = team1_weekly.loc[week]
        team2_fp = team2_weekly.loc[week]

        # Compare fantasy points and assign the result for each week
        if team1_fp > team2_fp:
            results.append(1)  # team1 wins
        else:
            results.append(0)  # team2 wins

    return results, common_weeks

def combine_team_data(team1_data, team2_data):
    """
    Combines data from two teams into one DataFrame and adds a 'result' column.
    The 'result' column indicates whether team1 won or lost (1 for win, 0 for loss).
    """
    game_results, common_weeks = derive_game_result(team1_data, team2_data)

    team1_data['result'] = team1_data['week'].apply(lambda x: game_results[common_weeks.get_loc(x)] if x in common_weeks else None)
    team2_data['result'] = team2_data['week'].apply(lambda x: 1 - game_results[common_weeks.get_loc(x)] if x in common_weeks else None)

    combined_data = pd.concat([team1_data, team2_data], ignore_index=True)

    return combined_data

def save_to_csv(data, filename):
    """
    Saves the filtered team data to a CSV file.
    """
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    years = [2022, 2021, 2020, 2019, 2018]
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
