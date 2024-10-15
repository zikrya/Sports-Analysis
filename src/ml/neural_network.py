import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout
from sklearn.model_selection import train_test_split

team_data = {
    "Philadelphia Eagles": {
        "team_morale": 5.0,
        "offensive_efficiency": 5.5,
        "defensive_performance": 6.0,
        "player_impact": {"Saquon Barkley": 5.5},
    },
    "Atlanta Falcons": {
        "team_morale": 4.8,
        "offensive_efficiency": 5.2,
        "defensive_performance": 5.8,
        "player_impact": {"Matt Ryan": 5.2},
    },
}

historical_ml_data = {
    "logistic_regression_accuracy": 0.5783,
    "random_forest_accuracy": 0.7607,
    "xgboost_accuracy": 0.9439,
    "log_loss": [0.68881, 0.68866, 0.68585, 0.68441],
}


def prepare_team_data(team_data):
    features = []
    for team, data in team_data.items():
        features.append(
            [
                data["team_morale"],
                data["offensive_efficiency"],
                data["defensive_performance"],
                list(data["player_impact"].values())[0],
            ]
        )
    return np.array(features)
a
def prepare_historical_data(ml_data):
    return np.array(
        [
            ml_data["logistic_regression_accuracy"],
            ml_data["random_forest_accuracy"],
            ml_data["xgboost_accuracy"],
        ]
    )

team_features = prepare_team_data(team_data)
ml_features = prepare_historical_data(historical_ml_data)

# Combining team data and historical ML data
X = np.hstack((team_features, np.tile(ml_features, (team_features.shape[0], 1))))

# Assume some labels (win/lose) for training purposes (1 for win, 0 for lose)
y = np.array([1, 0])

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


model = Sequential()
model.add(Input(shape=(X_train.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))  # Binary  (win/lose)


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=50, batch_size=2, verbose=1)


loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
