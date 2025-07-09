from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/") 
db = client["github_events"]
collection = db["events"]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == "push":
        author = data['pusher']['name']
        branch = data['ref'].split('/')[-1]
        timestamp = datetime.utcnow()
        collection.insert_one({
            "event_type": "push",
            "author": author,
            "to_branch": branch,
            "timestamp": timestamp
        })

    elif event_type == "pull_request":
        action = data['action']
        if action in ['opened', 'closed'] and data['pull_request'].get("merged", False):
            # It's a merge
            event = {
                "event_type": "merge",
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow()
            }
        else:
            # It's a pull request
            event = {
                "event_type": "pull_request",
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": datetime.utcnow()
            }
        collection.insert_one(event)

    return '', 204

@app.route('/events', methods=['GET'])
def get_events():
    result = []
    for event in collection.find().sort("timestamp", -1).limit(10):
        ts = event['timestamp'].strftime('%d %B %Y - %I:%M %p UTC')
        if event['event_type'] == "push":
            message = f"{event['author']} pushed to {event['to_branch']} on {ts}"
        elif event['event_type'] == "pull_request":
            message = f"{event['author']} submitted a pull request from {event['from_branch']} to {event['to_branch']} on {ts}"
        elif event['event_type'] == "merge":
            message = f"{event['author']} merged branch {event['from_branch']} to {event['to_branch']} on {ts}"
        else:
            message = "Unknown event"
        result.append(message)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
