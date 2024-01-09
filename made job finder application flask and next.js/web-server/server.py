from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

uri = "mongodb+srv://aymanelouazzani:ayman2002@cluster0.skjn4mk.mongodb.net/jobs_database?retryWrites=true&w=majority"
app.config["MONGO_URI"] = uri
mongo = PyMongo(app)

# Initialize a global variable to store the data
cached_data = []

# Function to fetch data from MongoDB and update the global variable
def fetch_data_from_mongodb():
    try:
        global cached_data
        data = mongo.db.get_collection("transformed_collection").find({}, {'_id': 0})
        cached_data = list(data)
        for id, job in enumerate(cached_data):
            job['id'] = id
            job['latitude'] = None if isinstance(job['latitude'], float) and math.isnan(job['latitude']) else job['latitude']
            job['longitude'] = None if isinstance(job['longitude'], float) and math.isnan(job['longitude']) else job['longitude']
        print("Data fetched and cached successfully.")
        print(cached_data[18])
    except Exception as e:
        print("Error fetching data:", str(e))

# Initial data fetch on server start
fetch_data_from_mongodb()

@app.route("/")
def lists():
    try:
        global cached_data
        return jsonify(cached_data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=5000)
