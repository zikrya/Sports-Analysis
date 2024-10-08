import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.api_nfl_data import fetch_team_data

def load_data(team_id_1, team_id_2):
    team_1_data = fetch_team_data(team_id_1)
    team_2_data = fetch_team_data(team_id_2)

    if team_1_data is None or team_2_data is None:
        print("Error fetching data from the API")
        return None

    combined_data = {
        'team_1': team_1_data,
        'team_2': team_2_data
    }

    data = pd.DataFrame([combined_data])
    print("Data loaded successfully from the API.")
    return data

if __name__ == "__main__":
    # Example usage
    team_id_1 = input("Enter Team 1 ID: ")
    team_id_2 = input("Enter Team 2 ID: ")
    data = load_data(team_id_1, team_id_2)

    if data is not None:
        print(data.head())

