# import libraries
import json
import pandas as pd
import numpy as np
from sklearn import datasets
from evidently.report import Report
from evidently.metrics import DataDriftTable
from evidently.metrics import DatasetDriftMetric
from evidently.pipeline.column_mapping import ColumnMapping

# Create a new instance of the ColumnMapping class
# See more : https://docs.evidentlyai.com/v/v0.1.57/features/dashboards/column_mapping
column_mapping = ColumnMapping()

# Set the target column name
column_mapping.target = 'class'

# Set the prediction column name
column_mapping.prediction = 'class'

# Set the list of numerical feature column names
numerical_features = ['education-num', 'age', 'hours-per-week', 'capital-gain']
column_mapping.numerical_features = numerical_features

# Set the list of categorical feature column names
categorical_features = ['education', 'occupation', 'native-country', 'workclass', 'marital-status', 'class']
column_mapping.categorical_features = categorical_features

# Fetch the dataset
adult_data = datasets.fetch_openml(name='adult', 
                                    version=2, 
                                    as_frame='auto')
# Transform into dataframe
adult = adult_data.frame


# Split the dataset for drift detection into reference and current data
adult_ref = adult[~adult.education.isin(['Some-college', 
                                        'HS-grad', 
                                        'Bachelors'])]
adult_cur = adult[adult.education.isin(['Some-college', 
                                        'HS-grad', 
                                        'Bachelors'])]

# Introduce missing values for demonstration
adult_cur.iloc[:2000, 3:5] = np.nan

# Initialize the report with desired metrics
data_drift_dataset_report = Report(metrics=[
    DatasetDriftMetric(),
    DataDriftTable(),  
])

# Run the report
data_drift_dataset_report.run(reference_data=adult_ref, 
                                current_data=adult_cur, 
                                column_mapping=column_mapping)

# Convert the JSON string to a Python dictionary for pretty printing
report_data = json.loads(data_drift_dataset_report.json())

# Save the report in JSON format with indentation for better readability
with open('data_drift_report.json', 'w') as f:
    json.dump(report_data, f, indent=4)

# save HTML
data_drift_dataset_report.save_html("Classification Report.html")

# in a notebook run :
# data_drift_dataset_report.show()