from flask import Flask, request, jsonify
import os
import json
import uuid
from git import Repo
import requests
from datetime import datetime

app = Flask(__name__)

# Path to store generated apps
GENERATED_APP_DIR = "generated_app"
os.makedirs(GENERATED_APP_DIR, exist_ok=True)

# Your GitHub repository path
REPO_PATH = os.getcwd()  # assuming repo is initialized here
repo = Repo(REPO_PATH)

@app.route("/api-endpoint", methods=["POST"])
def api_endpoint():
    try:
        data = request.get_json()
        print(f"Received request - Task: {data.get('task')}, Round: {data.get('round')}")
        print(f"Brief: {data.get('brief')}")

        # Verify secret (replace 'mysecret123' with your actual secret)
        if data.get("secret") != "mysecret123":
            return jsonify({"error": "Invalid secret"}), 403

        # Create/update index.html
        round_num = data.get("round", 1)
        index_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Auto-generated App - Round {round_num}</title>
        </head>
        <body>
            <h1>Auto-generated App</h1>
            <p>Round {round_num}</p>
            <p>Brief: {data.get('brief')}</p>
            <p>New features added!</p>
        </body>
        </html>
        """
        index_path = os.path.join(GENERATED_APP_DIR, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        print(f"✅ App saved at {index_path}")

        # Commit & push changes
        repo.git.add(A=True)
        if repo.is_dirty(untracked_files=True):
            commit_msg = f"Auto-update Round {round_num} - {datetime.now().isoformat()}"
            commit = repo.index.commit(commit_msg)
            origin = repo.remote(name='origin')
            origin.push()
            commit_sha = commit.hexsha
        else:
            commit_sha = repo.head.commit.hexsha
            print("No changes to commit.")

        # Send POST to evaluation URL
        evaluation_url = data.get("evaluation_url")
        if evaluation_url:
            payload = {
                "email": data.get("email"),
                "task": data.get("task"),
                "round": round_num,
                "nonce": data.get("nonce"),
                "repo_url": repo.remotes.origin.url,
                "commit_sha": commit_sha,
                "pages_url": f"https://{repo.remotes.origin.url.split('/')[-2]}.github.io/{repo.working_dir.split(os.sep)[-1]}/"
            }
            try:
                resp = requests.post(evaluation_url, json=payload, timeout=10)
                print(f"Evaluation POST response: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"Error posting to evaluation URL: {e}")
        else:
            print("⚠ No evaluation URL provided.")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
