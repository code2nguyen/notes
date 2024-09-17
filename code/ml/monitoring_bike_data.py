from tqdm import tqdm
import requests
import os
import zipfile
import datetime

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from evidently.report import Report
from evidently import ColumnMapping
from evidently.ui.workspace import Workspace
from evidently.metric_preset import RegressionPreset, DataDriftPreset, TargetDriftPreset

# ignore warnings
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

def download_file(url, save_path):
    """
    Downloads a file from the given URL and saves it to the specified path.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as file:
        for chunk in tqdm(response.iter_content(chunk_size=1024),
                          desc=f"Downloading {url}",
                          unit="B",
                          unit_scale=True,
                          unit_divisor=1024,
                          total=int(response.headers.get("content-length", 0))):
            file.write(chunk)

def load_data(zip_path, file_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        # Read a sample of the file as a DataFrame
        df = pd.read_csv(zip_file.open(file_name), header=0, sep=',', parse_dates=['dteday'])
    return df
    
def preprocess_data(raw_data):
    raw_data.index = raw_data.apply(lambda row: datetime.datetime.combine(row.dteday.date(), datetime.time(row.hr)),
                                    axis=1)
    return raw_data


def train_and_split_test(df, numerical_features, categorical_features, target):
    # Split the data into features and target variable
    X = df[numerical_features + categorical_features]
    y = df[target]

    # Split the data into training and validation sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize and train a Linear Regression model
    model = RandomForestRegressor(random_state = 0, n_estimators = 50)
    model.fit(X_train, y_train)

    # Make predictions on the training and validation sets
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    # Add the prediction column to the training and validation dataframes
    X_train['target'] = y_train
    X_train['prediction'] = train_preds

    X_test['target'] = y_test
    X_test['prediction'] = test_preds

    # Return the trained model and the training and validation data
    return model, X_train, X_test, y_train, y_test

def train_production_model(df, numerical_features, categorical_features, target):
    # Split the data into features and target variable
    X = df[numerical_features + categorical_features]
    y = df[target]

    # Initialize and train a Linear Regression model
    model = RandomForestRegressor(random_state = 0, n_estimators = 50)
    model.fit(X, y)

    return model

def generate_regression_performance_report(reference_data, current_data, column_mapping, name):
    regression_performance_report = Report(metrics=[
        RegressionPreset()

    ], metadata={"name": name})

    # Run the report
    regression_performance_report.run(reference_data=reference_data, 
                                      current_data=current_data, 
                                      column_mapping=column_mapping)
    
    return regression_performance_report


def generate_target_drift_report(reference_data, current_data, column_mapping, name):
    target_drift_report = Report(metrics=[
        TargetDriftPreset()

    ], metadata={"name": name})

    # Run the report
    target_drift_report.run(reference_data=reference_data, 
                                      current_data=current_data, 
                                      column_mapping=column_mapping)
    
    return target_drift_report

def generate_data_drift_report(reference_data, current_data, column_mapping, name):
    data_drift_report = Report(metrics=[
        DataDriftPreset()

    ], metadata={"name": name})

    # Run the report
    data_drift_report.run(reference_data=reference_data, 
                                      current_data=current_data, 
                                      column_mapping=column_mapping)
    
    return data_drift_report

def add_report_to_workspace(workspace, project_name, project_description, report):
    # Check if project already exists
    project = None
    for p in workspace.list_projects():
        if p.name == project_name:
            project = p
            break

    # Create a new project if it doesn't exist
    if project is None:
        project = workspace.create_project(project_name)
        project.description = project_description

    # Add report to the project
    workspace.add_report(project.id, report,)
    print(f"New report added to project {project_name}")

if __name__ == "__main__":
    WORKSPACE_NAME = "datascientest-workspace"
    PROJECT_NAME = "drift-monitoring-exam"
    PROJECT_DESCRIPTION = "Drift Monitoring Exam"
    file = r"https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"

    download_file(file, "data/bike_sharing_dataset.zip")

    raw_data = load_data("data/bike_sharing_dataset.zip", "hour.csv")
    raw_data = preprocess_data(raw_data)

    target = "cnt"
    prediction = 'prediction'
    numerical_features = ['temp', 'atemp', 'hum', 'windspeed', 'mnth', 'hr', 'weekday']
    categorical_features = ['season', 'holiday', 'workingday']

    column_mapping = ColumnMapping()
    column_mapping.target = 'target'
    column_mapping.prediction = 'prediction'
    column_mapping.numerical_features = numerical_features
    column_mapping.categorical_features = categorical_features

    
    reference_jan11 = raw_data.loc['2011-01-01 00:00:00':'2011-01-28 23:00:00']
    current_feb11 = raw_data.loc['2011-01-29 00:00:00':'2011-02-28 23:00:00']

    _, X_train, X_test, y_train, y_test = train_and_split_test(reference_jan11, numerical_features, categorical_features, target)

    workspace = Workspace(WORKSPACE_NAME)

    production_model = train_production_model(reference_jan11, numerical_features, categorical_features, target)
    reference_jan11["target"] = reference_jan11[target]
    reference_jan11["prediction"] = production_model.predict(reference_jan11[numerical_features + categorical_features])

    week1 = raw_data.loc['2011-01-29 00:00:00' : '2011-02-07 23:00:00']
    week2 = raw_data.loc['2011-02-07 00:00:00' : '2011-02-14 23:00:00']
    week3 = raw_data.loc['2011-02-15 00:00:00' : '2011-02-21 23:00:00']
    week1["target"] = week1[target]
    week2["target"] = week2[target]
    week3["target"] = week3[target]
    week1["prediction"] = production_model.predict(week1[numerical_features + categorical_features])
    week2["prediction"] = production_model.predict(week2[numerical_features + categorical_features])
    week3["prediction"] = production_model.predict(week3[numerical_features + categorical_features])

    vaildation_model_report = generate_regression_performance_report(X_train.sort_index(), X_test.sort_index(), column_mapping, "Model Validation Report")
    production_model_report = generate_regression_performance_report(reference_data=None, current_data=reference_jan11, column_mapping=column_mapping, name="Production Model Report")
    week1_report = generate_regression_performance_report(reference_data=None, current_data=week1, column_mapping=column_mapping, name="Week1 Model Report")
    week2_report = generate_regression_performance_report(reference_data=None, current_data=week2, column_mapping=column_mapping, name="Week2 Model Report")
    week3_report = generate_regression_performance_report(reference_data=None, current_data=week3, column_mapping=column_mapping, name="Week3 Model Report")
    target_driff_report = generate_target_drift_report(reference_data=reference_jan11, current_data=pd.concat([week1 , week2 , week3]), column_mapping=column_mapping, name="Target Drift Report")

    column_mapping_drift = ColumnMapping()

    column_mapping_drift.target = target
    column_mapping_drift.prediction = None
    column_mapping_drift.numerical_features = numerical_features
    column_mapping_drift.categorical_features = []

    data_driff_report = generate_data_drift_report(reference_data=reference_jan11, 
                                                   current_data=current_feb11.loc['2011-02-14 00:00:00':'2011-02-21 23:00:00'], 
                                                   column_mapping=column_mapping_drift, 
                                                   name="Data Drift Report")

    add_report_to_workspace(workspace, PROJECT_NAME, PROJECT_DESCRIPTION, vaildation_model_report)
    add_report_to_workspace(workspace, PROJECT_NAME, PROJECT_DESCRIPTION, production_model_report)
    add_report_to_workspace(workspace, PROJECT_NAME, PROJECT_DESCRIPTION, week1_report)
    add_report_to_workspace(workspace, PROJECT_NAME, PROJECT_DESCRIPTION, week2_report)
    add_report_to_workspace(workspace, PROJECT_NAME, PROJECT_DESCRIPTION, week3_report)
    add_report_to_workspace(workspace, PROJECT_NAME, PROJECT_DESCRIPTION, target_driff_report)
    add_report_to_workspace(workspace, PROJECT_NAME, PROJECT_DESCRIPTION, data_driff_report)
    
