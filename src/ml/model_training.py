import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
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
file_path = "matches.csv"
data = load_data(file_path)

if data is not None:
    # Drop non-numeric columns
    data = data.drop(columns=['date', 'notes'], errors='ignore')  # Drop 'notes' and 'date' columns if present

    # Handle missing values
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    imputer = SimpleImputer(strategy='mean')
    data[numeric_columns] = imputer.fit_transform(data[numeric_columns])

    #  Identify columns
    categorical_columns = data.select_dtypes(include=['object']).columns
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col].astype(str))

    # Define features
    X = data.drop(columns=['result'])
    y = data['result']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize the features for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Cross-Validation with StratifiedKFold ##
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Evaluate Logistic Regression with cross-validation
    logreg = LogisticRegression(max_iter=1000, penalty='l2', C=0.1)  # L2 regularization with C=0.1
    logreg_cv_scores = cross_val_score(logreg, X_train_scaled, y_train, cv=skf, scoring='accuracy')
    print(f"Cross-validated accuracy for Logistic Regression: {logreg_cv_scores.mean()}")

    # Evaluate Random Forest with cross-validation
    rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    rf_cv_scores = cross_val_score(rf, X_train, y_train, cv=skf, scoring='accuracy')
    print(f"Cross-validated accuracy for Random Forest: {rf_cv_scores.mean()}")

    # XGBoost with Early Stopping
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_test, label=y_test)

    params = {
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
        'alpha': 1.0
    }

    # XGBoost model with early stopping
    evals = [(dtrain, 'train'), (dval, 'eval')]
    xgb_model = xgb.train(params, dtrain, num_boost_round=500, evals=evals, early_stopping_rounds=10, verbose_eval=True)

    # Predictions using XGBoost
    y_pred_xgb = xgb_model.predict(dval)
    xgb_acc = accuracy_score(y_test, y_pred_xgb)
    xgb_f1 = f1_score(y_test, y_pred_xgb, average='weighted')

    print(f"XGBoost - Accuracy: {xgb_acc}, F1 Score: {xgb_f1}")

    # Cross-Validation
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=500,
        nfold=5,
        metrics={'mlogloss'},
        early_stopping_rounds=10,
        seed=42
    )
    print("XGBoost CV results:")
    print(cv_results)

    logreg.fit(X_train_scaled, y_train)
    y_pred_logreg = logreg.predict(X_test_scaled)
    logreg_acc = accuracy_score(y_test, y_pred_logreg)
    logreg_precision = precision_score(y_test, y_pred_logreg, average='weighted')
    logreg_recall = recall_score(y_test, y_pred_logreg, average='weighted')
    logreg_f1 = f1_score(y_test, y_pred_logreg, average='weighted')

    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, y_pred_rf)
    rf_precision = precision_score(y_test, y_pred_rf, average='weighted')
    rf_recall = recall_score(y_test, y_pred_rf, average='weighted')
    rf_f1 = f1_score(y_test, y_pred_rf, average='weighted')

    print(f"Logistic Regression - Accuracy: {logreg_acc}, Precision: {logreg_precision}, Recall: {logreg_recall}, F1 Score: {logreg_f1}")

    print(f"Random Forest - Accuracy: {rf_acc}, Precision: {rf_precision}, Recall: {rf_recall}, F1 Score: {rf_f1}")
