import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ml.data_loader import load_data

# Step 1: Load the data
file_path = "matches.csv"
data = load_data(file_path)

if data is not None:
    # Step 2: Drop non-numeric columns
    data = data.drop(columns=['date', 'notes'], errors='ignore')

    # Check missing values
    print("Missing values: ")
    print(data.isnull().sum())

    # Identify columns
    categorical_columns = data.select_dtypes(include=['object']).columns

    # Convert variables into numbers using Label Encoding
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col].astype(str))

    # Handle missing values using SimpleImputer
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    imputer = SimpleImputer(strategy='mean')
    data[numeric_columns] = imputer.fit_transform(data[numeric_columns])

    # Check for missing values after imputation
    print("Missing values after imputation:")
    print(data.isnull().sum())

    # Define features
    X = data.drop(columns=['result'])
    y = data['result']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize the features for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the Logistic Regression model
    logreg = LogisticRegression(max_iter=1000)
    logreg.fit(X_train_scaled, y_train)

    # Train the Random Forest model
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    #  Make predictions and evaluate the Logistic Regression model
    y_pred_logreg = logreg.predict(X_test_scaled)
    logreg_acc = accuracy_score(y_test, y_pred_logreg)
    logreg_f1 = f1_score(y_test, y_pred_logreg, average='weighted')

    # Make predictions and evaluate the Random Forest model
    y_pred_rf = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, y_pred_rf)
    rf_f1 = f1_score(y_test, y_pred_rf, average='weighted')

    print(f"Logistic Regression - Accuracy: {logreg_acc}, F1 Score: {logreg_f1}")
    print(f"Random Forest - Accuracy: {rf_acc}, F1 Score: {rf_f1}")
