# server.py
import os
import json
import subprocess
from flask import Flask, request, jsonify
from git import Repo
import requests

app = Flask(__name__)

# Configuration
REPO_PATH = os.path.join(os.getcwd())  # Current folder
GENERATED_APP_PATH = os.path.join(REPO_PATH, "generated_app")
INDEX_HTML_PATH = os.path.join(GENERATED_APP_PATH, "index.html")
REPO_URL = "https://github.com/achsah01/llm-project-demo.git"
PAGES_URL = "https://achsah01.github.io/llm-project-demo/"

# Ensure generated_app folder exists
os.makedirs(GENERATED_APP_PATH, exist_ok=True)

# Round templates
ROUND_HTML = {
    1: """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Auto-generated App</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        p {{ font-size: 1.2rem; }}
        .info {{ margin-top: 20px; padding: 10px; border: 1px solid #ccc; background: #f7f7f7; }}
    </style>
</head>
<body>
    <h1>Auto-generated App</h1>
    <p><strong>Brief:</strong> {brief}</p>
    <div class="info">
        <p>Round: 1</p>
        <p>Status: ✅ App generated successfully!</p>
    </div>
</body>
</html>""",
    2: """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Auto-generated App - Round 2</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        p {{ font-size: 1.2rem; }}
        .info {{ margin-top: 20px; padding: 10px; border: 1px solid #ccc; background: #f7f7f7; }}
    </style>
</head>
<body>
    <h1>Auto-generated App - Round 2</h1>
    <p><strong>Updated brief:</strong> {brief}</p>
    <div class="info">
        <p>New features added!</p>
        <p>Status: ✅ App updated successfully!</p>
    </div>
</body>
</html>"""
}


def write_index_html(round_num, brief):
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(ROUND_HTML[round_num].format(brief=brief))
    print(f"✅ App saved at {INDEX_HTML_PATH}")


def git_commit_and_push(commit_msg):
    repo = Repo(REPO_PATH)
    repo.git.add(A=True)
    if repo.is_dirty():
        repo.index.commit(commit_msg)
        origin = repo.remote(name='origin')
        origin.push()
        commit_sha = repo.head.commit.hexsha
        print(f"Commit SHA: {commit_sha}")
        return commit_sha
    else:
        print("No changes to commit.")
        return repo.head.commit.hexsha


def send_evaluation_post(payload):
    url = payload.get("evaluation_url")
    if not url or url.startswith("YOUR_EVALUATION_URL"):
        print("⚠ Invalid evaluation URL.")
        return
    try:
        resp = requests.post(url, json=payload, timeout=10)
        print(f"Evaluation POST response: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Error posting to evaluation URL: {e}")


@app.route("/api-endpoint", methods=["POST"])
def api_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Log raw request
    print("Received request - Task:", data.get("task"), "Round:", data.get("round"))
    print("Brief:", data.get("brief"))

    round_num = data.get("round", 1)
    brief = data.get("brief", "No brief provided")
    nonce = data.get("nonce", "")

    # Write the index.html based on round
    write_index_html(round_num, brief)

    # Commit & push changes to GitHub
    commit_sha = git_commit_and_push(f"Round {round_num} update: {brief}")

    # Send evaluation POST
    eval_payload = {
        "email": data.get("email", ""),
        "task": data.get("task", ""),
        "round": round_num,
        "nonce": nonce,
        "repo_url": REPO_URL,
        "commit_sha": commit_sha,
        "pages_url": PAGES_URL
    }
    send_evaluation_post(eval_payload)

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(port=5000)
