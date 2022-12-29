import pandas as pd
from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from numpy import ravel
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier

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

# Fit the model to the training data
model.fit(training_data, training_labels)

# Make predictions on the test data
labels = model.predict(testing_data)

accuracy = accuracy_score(ravel(testing_labels), ravel(labels))
print("Random Forest accuracy: ", accuracy)
# Accuracy: 0.9309834970905275

# ************ DECISION TREE ************
# Build the model
model = DecisionTreeClassifier(max_depth=5)

# Fit the model to the training data
model.fit(training_data, training_labels)

# Make predictions on the test data
labels = model.predict(testing_data)

accuracy = accuracy_score(ravel(testing_labels), ravel(labels))
print("Decision Tree accuracy: ", accuracy)
# Accuracy: 0.5884288848612038

# ************ K NEAREST NEIGHBOR ************
# Build the model
model = KNeighborsClassifier(n_neighbors=10)

# Fit the model to the training data
model.fit(training_data, training_labels)

# Make predictions on the test data
labels = model.predict(testing_data)

accuracy = accuracy_score(ravel(testing_labels), ravel(labels))
print("K Nearest Neighbor accuracy: ", accuracy)
# Accuracy: 0.4972336163312029

# ************ NAIVE BAYES ************
# Build the model
model = MultiOutputClassifier(GaussianNB())

# Fit the model to the training data
model.fit(training_data, training_labels)

# Make predictions on the test data
labels = model.predict(testing_data)

accuracy = accuracy_score(ravel(testing_labels), ravel(labels))
print("Naive Bayes accuracy: ", accuracy)
# Accuracy: 0.44672326624058


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
model = RandomForestClassifier(n_estimators=100)

# Fit the model to the training data from the dataset processed with PCA
model.fit(PCA_training_data, PCA_training_labels)

# Make predictions on the test data
labels = model.predict(PCA_testing_data)

accuracy = accuracy_score(ravel(PCA_testing_labels), ravel(labels))
print("Random forest accuracy: ", accuracy)
# Accuracy: 0.9026519126204331

# ************ DECISION TREE ************
# Build the model
model = DecisionTreeClassifier(max_depth=5)

# Fit the model to the training data
model.fit(PCA_training_data, PCA_training_labels)

# Make predictions on the test data
labels = model.predict(PCA_testing_data)

accuracy = accuracy_score(ravel(PCA_testing_labels), ravel(labels))
print("Decision Tree accuracy: ", accuracy)
# Accuracy: 0.6117523609653726

# ************ K NEAREST NEIGHBOR ************
# Build the model
model = KNeighborsClassifier(n_neighbors=10)

# Fit the model to the training data
model.fit(PCA_training_data, PCA_training_labels)

# Make predictions on the test data
labels = model.predict(PCA_testing_data)

accuracy = accuracy_score(ravel(PCA_testing_labels), ravel(labels))
print("K Nearest Neighbor accuracy: ", accuracy)
# Accuracy: 0.5960125918153201

# ************ NAIVE BAYES ************
# Build the model
model = MultiOutputClassifier(GaussianNB())

# Fit the model to the training data
model.fit(PCA_training_data, PCA_training_labels)

# Make predictions on the test data
labels = model.predict(PCA_testing_data)

accuracy = accuracy_score(ravel(PCA_testing_labels), ravel(labels))
print("Naive Bayes accuracy: ", accuracy)
# Accuracy: 0.491653152723457
