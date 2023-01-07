import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import ftplib
import csv

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


#FTP

# Open file in write mode
with open('coefficients.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Iterate over features and coefficients
    for feature, coef in zip(X.columns, model.coef_[0]):
        # Write feature and coefficient to file
        writer.writerow([feature, coef])
    # Convert intercept to string and remove brackets
    intercept_str = str(model.intercept_)
    intercept_str = intercept_str.strip('[]')
    # Write intercept to file
    writer.writerow(['intercept', intercept_str])


# Connect to FTP server
ftp_server = ftplib.FTP('185.114.108.114')
# Login to FTP server
ftp_server.login('niotron2023', 'csv_wow_2023!')

# Open file in binary read mode
with open('coefficients.csv', 'rb') as f:
    # Store file on FTP server
    ftp_server.storbinary('STOR coefficients.csv', f)
# Close FTP connection
ftp_server.quit()




print(accuracy)