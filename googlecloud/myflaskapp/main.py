import os
import subprocess
from flask import Flask
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import ftplib
import csv

app = Flask(__name__)

@app.route('/')
def run_script():
    subprocess.call(["python", "script.py"])
    return "Script ran successfully!"






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
