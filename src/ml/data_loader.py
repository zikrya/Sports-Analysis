import pandas as pd

def load_data(file_path):

    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

if __name__ == "__main__":
    file_path = "matches.csv"
    data = load_data(file_path)

    if data is not None:
        print(data.head())