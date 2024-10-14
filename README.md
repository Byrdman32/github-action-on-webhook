# GitHub Webhook Listener for Triggering Actions

This repository contains a Flask-based webhook listener designed to trigger GitHub Actions via the `repository_dispatch` event. It listens for specific GitHub events (e.g., `push` events), verifies webhook signatures using a secret token, and securely dispatches custom events to another GitHub repository to automate workflows.

## Features:

- **Webhook Listener**: A simple and efficient Flask app that listens for GitHub Webhooks.
- **Signature Verification**: Ensures security by verifying incoming webhook requests with HMAC-SHA256 signature validation using a shared secret.
- **Repository Dispatch**: Automatically triggers GitHub Actions in another repository by sending `repository_dispatch` events.
- **Custom Payloads**: Supports custom payloads to dynamically control what data is sent to the triggered GitHub Actions.
- **Deployment Ready**: Configured for easy deployment on Heroku or other cloud platforms.

## How It Works:

1. GitHub sends a `push` event or other selected events to the webhook.
2. The webhook validates the request signature using the secret token to ensure it's from GitHub.
3. Upon validation, the webhook triggers a custom event (`repository_dispatch`) on the specified GitHub repository, which can run an associated GitHub Action.

## Environment Variables:

This app uses environment variables for sensitive information like GitHub tokens and webhook secrets. To easily manage these, you can use a `.env` file.

### Example `.env` File:

You should create a `.env` file in the root of your project with the following content:

```bash
# GitHub Personal Access Token for authenticating the GitHub API requests
GITHUB_TOKEN=your_github_personal_access_token

# GitHub Repository owner and name for triggering repository_dispatch
REPOS=your_github_username_or_org/your_repository_name,your_github_username_or_org2/your_repository_name2,...

# Webhook Secret for verifying incoming GitHub webhooks
WEBHOOK_SECRET=your_webhook_secret_key

# Port for running Flask app
PORT=5000

# Event name for triggering repository_dispatch
EVENT_TYPE=your_trigger
```

### How to Use the `.env` File:

1. Create a file named `.env` in the root of your project.
2. Add the environment variables (GitHub token, repository owner, etc.) in the format above.
3. Ensure that the `.env` file is **not committed to version control**. Add it to `.gitignore` to prevent accidental commits.

## Installing and Running the App

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up your `.env` file (as described above) with your GitHub credentials and webhook secret.

3. Run the Flask app locally:

   ```bash
   python server.py
   ```
