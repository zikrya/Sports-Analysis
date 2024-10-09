import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import xgboost as xgb
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ml.data_loader import load_data

# Load data
file_path = "ATL_PHI_combined_weekly_data.csv"
data = load_data(file_path)

if data is not None:
    # Drop non-numeric columns
    data = data.drop(columns=['date', 'notes'], errors='ignore')

    # Handle missing values
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    imputer = SimpleImputer(strategy='mean')
    data[numeric_columns] = imputer.fit_transform(data[numeric_columns])

    # Identify categorical columns and encode them
    categorical_columns = data.select_dtypes(include=['object']).columns
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col].astype(str))

    # Convert the 'result' column to binary/multiclass target
    # Example for binary classification (adjust thresholds if needed)
    y = pd.cut(data['result'], bins=[-float('inf'), 0.5, float('inf')], labels=[0, 1])

    # If you want multiclass classification, use the following:
    # y = pd.cut(data['result'], bins=[-float('inf'), 0.33, 0.66, float('inf')], labels=[0, 1, 2])

    # Define features
    X = data.drop(columns=['result'])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize the features for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Cross-Validation with StratifiedKFold
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # GridSearchCV for Logistic Regression Hyperparameter Tuning
    logreg = LogisticRegression(max_iter=1000, penalty='l2')  # Base model
    logreg_params = {
        'C': [0.01, 0.1, 1, 10],
        'solver': ['newton-cg', 'lbfgs', 'liblinear']
    }
    grid_logreg = GridSearchCV(logreg, logreg_params, cv=skf, scoring='accuracy', n_jobs=-1)
    grid_logreg.fit(X_train_scaled, y_train)
    print(f"Best Logistic Regression Params: {grid_logreg.best_params_}")
    print(f"Best Logistic Regression Cross-Validated Accuracy: {grid_logreg.best_score_}")

    # GridSearchCV for Random Forest Hyperparameter Tuning
    rf = RandomForestClassifier(random_state=42)  # Base model
    rf_params = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_rf = GridSearchCV(rf, rf_params, cv=skf, scoring='accuracy', n_jobs=-1)
    grid_rf.fit(X_train, y_train)
    print(f"Best Random Forest Params: {grid_rf.best_params_}")
    print(f"Best Random Forest Cross-Validated Accuracy: {grid_rf.best_score_}")

    # XGBoost with Early Stopping
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_test, label=y_test)

    # XGBoost parameter tuning
    xgb_params = {
        'objective': 'multi:softmax',
        'eval_metric': 'mlogloss',
        'num_class': len(set(y)),
        'max_depth': 4,
        'eta': 0.01,
        'nthread': 4,
        'seed': 42,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'lambda': 2.0,
        'alpha': 1.0,
        'min_child_weight': 1
    }

    evals = [(dtrain, 'train'), (dval, 'eval')]
    xgb_model = xgb.train(xgb_params, dtrain, num_boost_round=500, evals=evals, early_stopping_rounds=10, verbose_eval=True)

    # XGBoost Hyperparameter Tuning with GridSearchCV
    xgb_grid_params = {
        'max_depth': [3, 4, 5],
        'min_child_weight': [1, 5, 10],
        'colsample_bytree': [0.3, 0.7, 1.0],
        'eta': [0.01, 0.05, 0.1]
    }
    xgb_cv_model = xgb.XGBClassifier(objective='multi:softmax', num_class=len(set(y)), eval_metric='mlogloss', seed=42)
    grid_xgb = GridSearchCV(xgb_cv_model, xgb_grid_params, cv=skf, scoring='accuracy', n_jobs=-1)
    grid_xgb.fit(X_train, y_train)
    print(f"Best XGBoost Params: {grid_xgb.best_params_}")
    print(f"Best XGBoost Cross-Validated Accuracy: {grid_xgb.best_score_}")

    # Evaluate the best models on test data
    best_logreg = grid_logreg.best_estimator_
    best_rf = grid_rf.best_estimator_
    best_xgb = grid_xgb.best_estimator_

    y_pred_logreg = best_logreg.predict(X_test_scaled)
    y_pred_rf = best_rf.predict(X_test)
    y_pred_xgb = best_xgb.predict(X_test)

    logreg_acc = accuracy_score(y_test, y_pred_logreg)
    logreg_f1 = f1_score(y_test, y_pred_logreg, average='weighted')

    rf_acc = accuracy_score(y_test, y_pred_rf)
    rf_f1 = f1_score(y_test, y_pred_rf, average='weighted')

    xgb_acc = accuracy_score(y_test, y_pred_xgb)
    xgb_f1 = f1_score(y_test, y_pred_xgb, average='weighted')

    print(f"Logistic Regression - Accuracy: {logreg_acc}, F1 Score: {logreg_f1}")
    print(f"Random Forest - Accuracy: {rf_acc}, F1 Score: {rf_f1}")
    print(f"XGBoost - Accuracy: {xgb_acc}, F1 Score: {xgb_f1}")
