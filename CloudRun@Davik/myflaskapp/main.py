import os
from flask import Flask
from script import execute

app = Flask(__name__)

@app.route('/')
def run_script():
    execute()
    return "Script ran successfully!"



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
