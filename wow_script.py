import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, explained_variance_score, confusion_matrix, accuracy_score, classification_report, log_loss, precision_score, recall_score
import ftplib
import csv

df = pd.read_csv("/Users/paoloartasensi/Python_Scripts/artabax/last_dataset.csv")

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

for feature, coef in zip(X.columns, model.coef_[0]):
    print('{},{}'.format(feature, coef))
print("b0,{}".format(intercept_str))


import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())


try:
    service = build("drive", "v3", credentials=creds)
    response = service.files().list(
        q="name= 'uploadpython' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive'
    ).execute()
    if not response['files']:
        file_metadata = {
            "name": "uploadpython",
            "mimeType": "application/vnd.google-apps.folder"}
        file = service.files().create(body=file_metadata, fields="id").execute()
        folder_id = file.get('id')
    else:
        folder_id = response['files'][0]['id']
except HttpError as e:
    print("Error: " + str(e))



import csv
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

csv_file = open('coefficients.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
for feature, coef in zip(X.columns, model.coef_[0]):
    csv_writer.writerow([feature, coef])
intercept_str = str(model.intercept_).strip('[]')
csv_writer.writerow(['intercept', intercept_str])
csv_file.close()


FOLDER_ID = '1RS6V6qWHL7gd1zP2GT7IKOlOPb1Y1YZt'
def upload_file(service, file_path, folder_id=None):
    file_name = 'coefficients.csv'
    query = f"name='{file_name}' and trashed = false"
    if folder_id:
        query += f" and parents in '{folder_id}'"
    files = service.files().list(q=query, spaces='drive').execute()
    existing_files = files.get('files', [])
    for file in existing_files:
        service.files().delete(fileId=file['id']).execute()

    file_metadata = {'name': file_name, 'mimeType': 'text/csv'}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, mimetype='text/csv', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media).execute()
    print(F'File ID: {file.get("id")}')
upload_file(service, 'coefficients.csv', FOLDER_ID)



