# README, this is a copy of the orginal scritp file stored in "MyFlask" Google Project,
# on Google Cloud Run service, it works with main.py FLASK APP 
# it will run the Machine Learning and put the file to FTP
# WARNING, it works from anywhere!

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import ftplib
import json

url = 'https://dev.paoloartasensi.it/python/csv/last_dataset.csv'
df = pd.read_csv(url)

X = df[['ax', 'ay', 'az', 'gx', 'gy', 'gz','pitch','roll', 'BAR','totacc' ]]
y = df['status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
intercept_str = str(model.intercept_).strip('[]')


# Open file in write mode
with open('coefficients.json', 'w') as jsonfile:
    # Initialize an empty dictionary to store the information
    data = {}
    # Iterate over features and coefficients
    for feature, coef in zip(X.columns, model.coef_[0]):
        # Add feature and coefficient to dictionary
        data[feature] = coef

    # Add intercept to dictionary
    data['intercept'] = model.intercept_[0]
    # Write dictionary to file
    json.dump(data, jsonfile)


# Connect to FTP server
ftp_server = ftplib.FTP('185.114.108.114')
# Login to FTP server
ftp_server.login('niotron2023', 'csv_wow_2023!')

# Open the 'coefficients.json' file in binary mode
with open('coefficients.json', 'rb') as jsonfile:
    # Store the file on the FTP server
    ftp_server.storbinary('STOR coefficients.json', jsonfile)
    # Close FTP connection
ftp_server.quit()
