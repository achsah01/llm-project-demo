from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# ----------------------------
# Configuration
# ----------------------------
SECRET = "mysecret123"
GITHUB_USERNAME = "achsah01"
REPO_NAME = "llm-project-demo"
PAGES_URL = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"

# ----------------------------
# API Endpoint
# ----------------------------
@app.route("/api-endpoint", methods=["POST"])
def api_endpoint():
    # Debug: print raw data and headers
    print("Raw data received:", request.data)
    print("Headers:", request.headers)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    # Verify secret
    if data.get("secret") != SECRET:
        return jsonify({"status": "error", "message": "Invalid secret"}), 403

    # Extract fields
    task = data.get("task", "demo-task")
    round_num = data.get("round", 1)
    brief = data.get("brief", "")
    nonce = data.get("nonce", "demo-nonce")
    evaluation_url = data.get("evaluation_url")

    print(f"Received request - Task: {task}, Round: {round_num}")
    print("Brief:", brief)

    # ----------------------------
    # Generate or update app
    # ----------------------------
    app_folder = "generated_app"
    os.makedirs(app_folder, exist_ok=True)

    if round_num == 1:
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Generated App</title></head>
        <body>
        <h1>Auto-generated App</h1>
        <p>Brief: {brief}</p>
        </body>
        </html>
        """
    elif round_num == 2:
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Updated App - Round 2</title></head>
        <body>
        <h1>Auto-generated App - Round 2</h1>
        <p>Updated brief: {brief}</p>
        <p>New features added!</p>
        </body>
        </html>
        """
    else:
        return jsonify({"status": "error", "message": "Invalid round number"}), 400

    # Write HTML
    index_path = os.path.join(app_folder, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"✅ App saved at {index_path}")

    # ----------------------------
    # Get latest commit SHA
    # ----------------------------
    commit_sha = ""
    try:
        commit_sha = os.popen("git rev-parse HEAD").read().strip()
        print(f"Commit SHA: {commit_sha}")
    except Exception as e:
        print("Error getting commit SHA:", e)

    # ----------------------------
    # Notify evaluation URL
    # ----------------------------
    if evaluation_url:
        payload = {
            "email": "23f3003822@ds.study.iitm.ac.in",
            "task": task,
            "round": round_num,
            "nonce": nonce,
            "repo_url": f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}",
            "commit_sha": commit_sha,
            "pages_url": PAGES_URL
        }
        try:
            resp = requests.post(evaluation_url, json=payload, timeout=10)
            print("Evaluation POST response:", resp.status_code, resp.text)
        except Exception as e:
            print("Error posting to evaluation URL:", e)

    return jsonify({"status": "ok", "message": f"App processed and evaluation notified for round {round_num}"}), 200

# ----------------------------
# Health check
# ----------------------------
@app.route("/", methods=["GET"])
def health():
    return "Server is running!", 200

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
