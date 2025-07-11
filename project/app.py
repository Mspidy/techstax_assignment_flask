


from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# MongoDB Connection
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
        timestamp = datetime.now(timezone.utc)
        commit_message = data['head_commit']['message'] if 'head_commit' in data else 'No message'
        collection.insert_one({
            "event_type": "push",
            "author": author,
            "to_branch": branch,
            "timestamp": timestamp
        })

    elif event_type == "pull_request":
        action = data['action']
        pr = data['pull_request']
        author = pr['user']['login']
        from_branch = pr['head']['ref']
        to_branch = pr['base']['ref']
        timestamp = datetime.now(timezone.utc)
        title = pr.get('title', 'No Title')
        body = pr.get('body', 'No Description')

        if action == "closed" and pr.get("merged", False):
            event = {
                "event_type": "merge",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "title": title,
                "body": body
            }
        elif action == "opened":
            event = {
                "event_type": "pull_request",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "title": title,
                "body": body
            }
        else:
            return '', 204  # Ignore other actions
        collection.insert_one(event)

    return '', 204

# @app.route('/events', methods=['GET'])
# def get_events():
#     result = []
#     for event in collection.find().sort("timestamp", -1).limit(10):
#         print(event)
#         ts = event['timestamp'].strftime('%d %B %Y - %I:%M %p UTC')
#         if event['event_type'] == "push":
#             message = f"{event['author']} pushed to {event['to_branch']} on {ts}"
#         elif event['event_type'] == "pull_request":
#             message = f"{event['author']} submitted a pull request from {event['from_branch']} to {event['to_branch']} on {ts}"
#         elif event['event_type'] == "merge":
#             message = f"{event['author']} merged branch {event['from_branch']} to {event['to_branch']} on {ts}"
#         else:
#             message = "Unknown event"
#         result.append(message)
#     return jsonify(result)

@app.route('/events', methods=['GET'])
def get_events():
    events = []
    for event in collection.find().sort("timestamp", -1).limit(10):
        event['_id'] = str(event['_id'])  # Optional: make ObjectId JSON serializable
        events.append(event)
    return jsonify(events)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
