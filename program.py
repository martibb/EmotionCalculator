import pandas as pd
from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from numpy import ravel
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import shap


data = read_csv('data/preprocessed.csv')
data = data.drop(['timestamp', 'pid'], axis=1)
data.to_csv('data/preprocessedWholeData.csv', index=False)
data = read_csv('data/preprocessedWholeData.csv')

X = data.iloc[:, :len(data.columns) - 2]
y = data[['arousal', 'valence']]

training_data, testing_data, training_labels, testing_labels = train_test_split(X, y, test_size=0.2, random_state=0)

# ************ RANDOM FOREST ************
# Build the model
model1 = RandomForestClassifier(n_estimators=100)

# Fit the model to the training data
model1.fit(training_data, training_labels)

# Make predictions on the test data
labels = model1.predict(testing_data)

accuracy = accuracy_score(ravel(testing_labels), ravel(labels))
print("Random Forest accuracy: ", accuracy)
# Accuracy: 0.9309834970905275


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


# The columns related to each individual sensor will be separated. In fact, we want to reduce to one column per sensor
# the function called also performs data scaling, which is necessary to apply PCA.
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

PCA_X = PCA_data.iloc[:, :len(PCA_data.columns) - 2]

PCA_training_data, PCA_testing_data, PCA_training_labels, PCA_testing_labels = train_test_split(PCA_X, y, test_size=0.2,
                                                                                                random_state=0)
print("\n")
print("Processing after Principal Component Analysis (PCA):")

# ************ RANDOM FOREST ************
# Build the model
model2 = RandomForestClassifier(n_estimators=100)

# Fit the model to the training data from the dataset processed with PCA
model2.fit(PCA_training_data, PCA_training_labels)

# Make predictions on the test data
labels = model2.predict(PCA_testing_data)

accuracy = accuracy_score(ravel(PCA_testing_labels), ravel(labels))
print("Random forest accuracy: ", accuracy)
# Accuracy: 0.9026519126204331


# ************ GENERAL FEATURE IMPORTANCE ************
# Get the feature importances from the model
importances = model1.feature_importances_

# Sort the feature importances in descending order
indices = np.argsort(importances)[::-1]

# Rearrange the feature names so they match the sorted feature importances
names = [X.columns[i] for i in indices]

# Create a bar plot of the feature importances
plt.bar(range(X.shape[1]), importances[indices])

# Add feature names as x-axis labels
plt.xticks(range(X.shape[1]), names, rotation=90)

# Show the plot
plt.show()


# ************ GENERAL FEATURE IMPORTANCE (PCA) ************
# Get the feature importances from the model
importances = model2.feature_importances_

# Sort the feature importances in descending order
indices = np.argsort(importances)[::-1]

# Rearrange the feature names so they match the sorted feature importances
names = [PCA_X.columns[i] for i in indices]

# Create a bar plot of the first 6 feature importances
plt.bar(range(6), importances[indices][:6])

# Add feature names as x-axis labels
plt.xticks(range(6), names[:6], rotation=90)

# Show the plot
plt.show()


# ************ ROW FEATURE IMPORTANCE ************
# Choose an input row to explain
row_to_explain = testing_data.iloc[0, :]

# Explain the prediction for the "arousal" target column using SHAP
explainer = shap.TreeExplainer(model1)
shap_values = explainer.shap_values(row_to_explain)

# Print the feature importances for the "arousal" target column
print("\nSHAP feature importances for 'arousal' target:")
for i, importance in enumerate(shap_values[0]):
    print(X.columns[i], ":", importance)

# Explain the prediction for the "valence" target column using SHAP
explainer = shap.TreeExplainer(model1)
shap_values = explainer.shap_values(row_to_explain)

# Print the feature importances for the "valence" target column
print("\nSHAP feature importances for 'valence' target:")
for i, importance in enumerate(shap_values[1]):
    print(X.columns[i], ":", importance)


# ************ ROW FEATURE IMPORTANCE (PCA) ************
# Choose an input row to explain
row_to_explain = PCA_testing_data.iloc[0, :]

# Explain the prediction for the "arousal" target column using SHAP
explainer = shap.TreeExplainer(model2)
shap_values = explainer.shap_values(row_to_explain)

# Print the feature importances for the "arousal" target column
print("\nSHAP feature importances for 'arousal' target:")
for i, importance in enumerate(shap_values[0]):
    print(PCA_X.columns[i], ":", importance)

# Explain the prediction for the "valence" target column using SHAP
explainer = shap.TreeExplainer(model2)
shap_values = explainer.shap_values(row_to_explain)

# Print the feature importances for the "valence" target column
print("\nSHAP feature importances for 'valence' target:")
for i, importance in enumerate(shap_values[1]):
    print(PCA_X.columns[i], ":", importance)


