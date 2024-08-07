# -*- coding: utf-8 -*-
"""xgBOOST.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TTQaykDBOWD7pPHUsH0jUBONuN6qo_Wd
"""

import pandas as pd
import numpy as np

import xgboost as xgb

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("/content/drive/My Drive/data/heart_attack_prediction_dataset.csv")
df.head()

df = df.drop(columns = ["Patient ID", "Continent", "Hemisphere"])
df[['systolic', 'diastolic']] = df['Blood Pressure'].str.split('/', expand=True).astype(int)
df = df.drop(columns = ["Blood Pressure"])
df.info()

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
columns_to_encode = ["Sex", "Diet", "Country"]
for col in columns_to_encode:
  df[col] = encoder.fit_transform(df[col])
df.info()

X = df.drop(columns = ["Heart Attack Risk"])
y = df["Heart Attack Risk"]

"""**XGBOOST**"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 43, stratify = y)

import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

from sklearn.metrics import accuracy_score

parameters_grid = {
    'max_depth': [2, 4, 6, 8, 10],
    'learning_rate': [0.01, 0.02, 0.04, 0.06, 0.08, 1.0],
    'n_estimators': [10, 20, 30, 40, 50, 60, 70 , 80 , 90],
    'subsample': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
}

"""**USING RANDOMIZEDSEARCHCV**"""

xgb = xgb.XGBClassifier()
r_xgb = RandomizedSearchCV(xgb, parameters_grid, cv=5, scoring='accuracy', n_iter=10, random_state = 42, verbose = 3)

r_xgb.fit(X_train, y_train)

predictions = r_xgb.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, predictions)}")

print("Best parameters found: ", r_xgb.best_params_)
print("Lowest RMSE found: ", np.sqrt(np.abs(r_xgb.best_score_)))

from sklearn.metrics import confusion_matrix, classification_report
print(f"Confusion Matrix \n {confusion_matrix(y_test, predictions)}")
print(f"Classification Report \n {classification_report(y_test, predictions)}")

df["Heart Attack Risk"].value_counts()

"""The model is performing poorly on the 1 class, due to class imbalace. Using accuracy as a scoring metric can be  misleading as an high accuracy does not signify the performance of the model on both classes as seen above.
Scoring will be set to f1 to select the best model

**USING F1 AS THE SCORING METRIC IN THE RANDOMIZEDSEARCHCV**
"""

xgb_f1 = RandomizedSearchCV(xgb, parameters_grid, cv=5, scoring='f1', n_iter=10, random_state = 42, verbose = 3)

xgb_f1.fit(X_train, y_train)

xgb_f1_predictions = xgb_f1.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, xgb_f1_predictions)}")

print("Best parameters found: ", xgb_f1.best_params_)
print("Lowest RMSE found: ", np.sqrt(np.abs(xgb_f1.best_score_)))

from sklearn.metrics import confusion_matrix, classification_report
print(f"Confusion Matrix \n {confusion_matrix(y_test, xgb_f1_predictions)}")
print(f"Classification Report \n {classification_report(y_test, xgb_f1_predictions)}")