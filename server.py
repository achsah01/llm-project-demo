from flask import Flask, request, jsonify
import os
from git import Repo
import requests

app = Flask(__name__)

SECRET = "mysecret123"
REPO_PATH = os.path.abspath(".")
GENERATED_APP_PATH = os.path.join(REPO_PATH, "generated_app", "index.html")


@app.route("/api-endpoint", methods=["POST"])
def handle_post():
    data = request.get_json(force=True)
    round_num = data.get("round")
    secret = data.get("secret")
    brief = data.get("brief", "No brief provided")
    eval_url = data.get("evaluation_url", "")
    task = data.get("task", "demo-task")

    print(f"Received request - Task: {task}, Round: {round_num}")
    print(f"Brief: {brief}")

    # Validate secret
    if secret != SECRET:
        print("❌ Invalid secret received.")
        return jsonify({"error": "Invalid secret"}), 403

    # Generate HTML content based on round
    if round_num == 1:
        content = f"<h1>Auto-generated App - Round 1</h1><p>Brief: {brief}</p>"
    elif round_num == 2:
        content = f"<h1>Auto-generated App - Round 2</h1><p>Updated brief: {brief}</p><p>New features added!</p>"
    else:
        content = f"<h1>Unknown round</h1><p>Brief: {brief}</p>"

    # Save generated HTML
    os.makedirs(os.path.dirname(GENERATED_APP_PATH), exist_ok=True)
    with open(GENERATED_APP_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ App saved at {GENERATED_APP_PATH}")

    # Commit and push to GitHub
    try:
        repo = Repo(REPO_PATH)
        repo.git.add(A=True)
        if repo.is_dirty():
            repo.index.commit(f"Auto-update for round {round_num}")
            origin = repo.remote(name="origin")
            origin.push()
            print("✅ Changes pushed to GitHub")
        else:
            print("No changes to commit.")
    except Exception as e:
        print(f"⚠ Git error: {e}")

    # POST back to evaluation URL
    if eval_url:
        try:
            resp = requests.post(eval_url, json={"round": round_num, "status": "done"})
            print(f"Evaluation POST response: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"⚠ Could not reach evaluation URL: {e}")
    else:
        print("⚠ Invalid evaluation URL.")

    return jsonify({"status": "success", "round": round_num}), 200


if __name__ == "__main__":
    app.run(port=5000)
