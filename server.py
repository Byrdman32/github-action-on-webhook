from flask import Flask, request, jsonify, abort
import requests
import json
import os
import hmac
import hashlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch environment variables from .env or system environment
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPOS = os.getenv('REPOS', '').split(',')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
EVENT_TYPE = os.getenv('EVENT_TYPE')

# GitHub API Headers
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def trigger_repository_dispatch(repo_owner, repo_name, message, passed):
    """Trigger the workflow dispatch event for a specific repository."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dispatches"

    if not GITHUB_TOKEN or not repo_owner or not repo_name:
        print("Error: Missing environment variables or configuration.")
        return

    data = {
        "event_type": EVENT_TYPE,
        "client_payload": {
            "passed": passed,
            "message": message
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 204:
            print(f"Repository Dispatch event triggered successfully for {repo_owner}/{repo_name}!")
        else:
            print(f"Failed to trigger Repository Dispatch for {repo_owner}/{repo_name}. Status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {repo_owner}/{repo_name}: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {repo_owner}/{repo_name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {repo_owner}/{repo_name}: {e}")

def verify_signature(request):
    """Verify the GitHub webhook signature using the secret."""
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        print("Missing signature")
        abort(400, "Signature missing")

    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        print("Wrong hash type")
        abort(400, "Wrong hash type")

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        print("Signature mismatch")
        abort(400, "Signature mismatch")

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Route to handle the GitHub webhook and trigger the dispatch."""
    # Verify the request signature
    verify_signature(request)

    if request.method == 'POST':
        payload = request.json

        if payload.get('ref') and payload['ref'] == 'refs/heads/main':
            print("Push event detected on main branch")
            pusher = payload.get('pusher', {}).get('name', 'Unknown user')
            commit_message = payload.get('head_commit', {}).get('message', 'No commit message')

            # Loop through all the repositories listed in .env and trigger dispatch for each
            for repo in REPOS:
                repo_owner, repo_name = repo.split('/')
                trigger_repository_dispatch(repo_owner, repo_name, message=f"Pushed by {pusher}: {commit_message}", passed=True)

        return jsonify({'status': 'received'}), 200
    else:
        return jsonify({'error': 'Invalid method'}), 405

# Catch-all route to handle any undefined routes
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "This route is not defined. Please use a valid route!"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
