import time
import numpy as np
import pandas as pd
import shap
from matplotlib import pyplot as plt
from matplotlib import use as matplotlib_use
from pandas import read_csv
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

path = ''

data = read_csv('data/preprocessed.csv')
data = data.drop(['timestamp', 'pid'], axis=1)
data.to_csv('data/preprocessedWholeData.csv', index=False)
data = read_csv('data/preprocessedWholeData.csv')

X = data.iloc[:, :len(data.columns) - 2]
y = data[['arousal', 'valence']]

training_data, testing_data, training_labels, testing_labels = train_test_split(X, y, test_size=0.2, random_state=0)

# ************ RANDOM FOREST ************
# Build the model
model = RandomForestClassifier(n_estimators=100)

model.fit(training_data, training_labels)


# ***************************** PCA *****************************
# THIS FUNCTION SEPARATES INDIVIDUAL SENSOR COLUMNS AND ALSO SCALES THE DATA
def separate_sensor_columns(dataset, sensor_name):
    # E4 bracelet is multi-sensor: it measures three-axis acceleration, photoplethysmography from which it also derives
    # blood volume pulse (BVP), heart rate (HR), intra-beat interval (IBI) and also measures body temperature (TEMP)
    # and electrodermal activity (EDA)
    if sensor_name == 'E4_ACC':
        sensor_columns = dataset[['x', 'y', 'z']]
        return sensor_columns
    if sensor_name == 'E4_HR':
        sensor_columns = dataset[['E4_BVP', 'E4_HR']]
        return sensor_columns
    if sensor_name == 'E4_TEMP':
        sensor_columns = dataset[['E4_TEMP']]
        return sensor_columns
    if sensor_name == 'E4_EDA':
        sensor_columns = dataset[['E4_EDA']]
        return sensor_columns
    # EEG sensor collects frequency data on 8 different bands
    elif sensor_name == 'EEG':
        sensor_columns = dataset[
            ['delta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'middleGamma', 'theta']]
        scaled_columns = StandardScaler().fit_transform(sensor_columns)
        return scaled_columns
    # eSense sensor collects frequency data on attention and meditation
    elif sensor_name == 'eSense':
        sensor_columns = dataset[['Attention', 'Meditation']]
        scaled_columns = StandardScaler().fit_transform(sensor_columns)
        return scaled_columns


def process_PCA():
    # The columns related to each individual sensor will be separated. In fact, we want to reduce to one column per
    # sensor the function called also performs data scaling, which is necessary to apply PCA.
    E4_ACC = separate_sensor_columns(data, 'E4_ACC')
    E4_HR = separate_sensor_columns(data, 'E4_HR')
    E4_TEMP = separate_sensor_columns(data, 'E4_TEMP')
    E4_EDA = separate_sensor_columns(data, 'E4_EDA')
    EEG = separate_sensor_columns(data, 'EEG')
    eSense = separate_sensor_columns(data, 'eSense')

    # Now with the PCA technique we reduce to 1 component (column)
    pca = PCA(n_components=1)

    E4_ACC_PCA = pca.fit_transform(E4_ACC)
    E4_HR_PCA = pca.fit_transform(E4_HR)
    E4_TEMP_PCA = pca.fit_transform(E4_TEMP)
    E4_EDA_PCA = pca.fit_transform(E4_EDA)
    EEG_PCA = pca.fit_transform(EEG)
    eSense_PCA = pca.fit_transform(eSense)

    # I report the data in the form of a dataframe column by column
    E4_ACC_DF = pd.DataFrame(data=E4_ACC_PCA, columns=['E4_ACC'])
    E4_HR_DF = pd.DataFrame(data=E4_HR_PCA, columns=['E4_Fotopletismography'])
    E4_TEMP_DF = pd.DataFrame(data=E4_TEMP_PCA, columns=['E4_TEMP'])
    E4_EDA_DF = pd.DataFrame(data=E4_EDA_PCA, columns=['E4_EDA'])
    EEG_DF = pd.DataFrame(data=EEG_PCA, columns=['EEG'])
    eSense_DF = pd.DataFrame(data=eSense_PCA, columns=['eSense'])
    # Columns in dataframe format will be merged to form a single dataframe
    PCA_data = pd.concat([E4_ACC_DF, E4_HR_DF, E4_TEMP_DF, E4_EDA_DF, EEG_DF, eSense_DF, y], axis=1)
    return PCA_data


PCA_data = process_PCA()
PCA_X = PCA_data.iloc[:, :len(PCA_data.columns) - 2]

PCA_training_data, PCA_testing_data, PCA_training_labels, PCA_testing_labels = train_test_split(PCA_X, y, test_size=0.2,
                                                                                                random_state=0)

# ************ RANDOM FOREST ************
# Build the model
PCA_model = RandomForestClassifier(n_estimators=100)

PCA_model.fit(PCA_training_data, PCA_training_labels)

# ************ GENERAL FEATURE IMPORTANCE ************
# Get the feature importances from the model
importances = model.feature_importances_

# Sort the feature importances in descending order
indices = np.argsort(importances)[::-1]

# Rearrange the feature names, so they match the sorted feature importances
names = [X.columns[i] for i in indices]

# Create a bar plot of the feature importances
plt.figure()
plt.bar(range(X.shape[1]), importances[indices])

# Add feature names as x-axis labels
plt.xticks(range(X.shape[1]), names, rotation=90)

# Save the plot to an image file
plt.savefig('static/img/generalFI.png')

# ************ GENERAL FEATURE IMPORTANCE (PCA) ************
# Get the feature importances from the model
importances = PCA_model.feature_importances_

# Sort the feature importances in descending order
indices = np.argsort(importances)[::-1]

# Rearrange the feature names, so they match the sorted feature importances
names = [PCA_X.columns[i] for i in indices]

# Create a bar plot of the first 6 feature importances
plt.figure()
plt.bar(range(6), importances[indices][:6])

# Add feature names as x-axis labels
plt.xticks(range(6), names[:6], rotation=90)

# Save the plot to an image file
plt.savefig('static/img/PCAFI.png')


# **************************************** Functions **********************************************
def get_components_properties(type):
    if type == "general":
        df = data
    else:
        df = PCA_data

    # Find the minimum value of each column
    min_values = df.min()

    # Find the maximum value of each column
    max_values = df.max()

    results = {}
    # Iterate through each column
    for col in df.columns:
        # Convert min and max values to integers
        min_value = min_values[col]

        max_value = max_values[col]

        # Create a dictionary for each column with min and max values as values
        results[col] = {'min': min_value, 'max': max_value}

    return results


def classify(set):
    # Convert the test dictionary into a 2D array-like object
    data = pd.DataFrame([set])

    # Rearrange the columns of the test data to match the column order of the training data
    data = data.reindex(columns=training_data.columns)

    labels = model.predict(data)

    return labels


def PCA_classify(set):
    # Convert the test dictionary into a 2D array-like object
    data = pd.DataFrame([set])

    # Rearrange the columns of the test data to match the column order of the training data
    data = data.reindex(columns=PCA_training_data.columns)

    labels = PCA_model.predict(data)

    return labels


def compute_row_feature_importance(mode, rows):
    matplotlib_use('Agg')

    if mode == "General":
        rows = pd.Series(rows)
        print(rows)

        keys = ['E4_BVP', 'E4_EDA', 'E4_HR', 'E4_TEMP', 'x', 'y', 'z', 'Attention', 'delta', 'lowAlpha', 'highAlpha',
                'lowBeta', 'highBeta', 'lowGamma', 'middleGamma', 'theta', 'Meditation']
        rows = rows.reindex(keys)

        # Explain the prediction for the "arousal" target column using SHAP
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(rows)

        # Explain the prediction for the "valence" target column using SHAP
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(rows)

        # Create a bar plot of the SHAP feature importances for both target columns
        importances_arousal = shap_values[0]
        importances_valence = shap_values[1]
        features = X.columns

        fig, ax = plt.subplots()
        ax.barh(features, importances_arousal, label="Arousal")
        ax.barh(features, importances_valence, label="Valence")

        plt.title("SHAP Feature Importances for 'arousal' and 'valence' Targets")
        plt.ylabel("Feature")
        plt.xlabel("Importance")
        plt.legend()

        # Save the plot to an image file
        plt.savefig('static/img/generalRowFI.png')

    else:  # mode == "PCA"
        rows = pd.Series(rows)

        keys = ['E4_ACC', 'E4_Fotopletismography', 'E4_TEMP', 'E4_EDA', 'EEG', 'eSense']
        rows = rows.reindex(keys)

        # Explain the prediction for the "arousal" target column using SHAP
        explainer = shap.TreeExplainer(PCA_model)
        shap_values = explainer.shap_values(rows)

        # Explain the prediction for the "valence" target column using SHAP
        explainer = shap.TreeExplainer(PCA_model)
        shap_values = explainer.shap_values(rows)

        # Create a bar plot of the SHAP feature importances for both target columns
        importances_arousal = shap_values[0]
        importances_valence = shap_values[1]
        features = PCA_X.columns

        fig, ax = plt.subplots()
        ax.barh(features, importances_arousal, label="Arousal")
        ax.barh(features, importances_valence, label="Valence")

        plt.title("SHAP Feature Importances for 'arousal' and 'valence' Targets")
        plt.ylabel("Feature")
        plt.xlabel("Importance")
        plt.legend()

        path = 'static/img/PCARowFI.png'

        plt.savefig(path)
