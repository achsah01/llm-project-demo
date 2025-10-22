from flask import Flask, request, jsonify
import os, requests, subprocess

app = Flask(__name__)

SECRET = os.environ.get("SECRET_KEY", "mysecret123")

@app.route("/api-endpoint", methods=["POST"])
def api_endpoint():
    data = request.get_json()
    print(f"Received request - Task: {data.get('task')}, Round: {data.get('round')}")
    print(f"Brief: {data.get('brief')}")

    # Secret verification
    if data.get("secret") != SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    round_number = data.get("round")
    brief = data.get("brief", "")
    evaluation_url = data.get("evaluation_url", "")

    # Generate app file (simulate)
    os.makedirs("generated_app", exist_ok=True)
    index_html_path = os.path.join("generated_app", "index.html")
    html_content = f"""
    <html>
    <head><title>Auto-generated App - Round {round_number}</title></head>
    <body>
    <h1>Auto-generated App - Round {round_number}</h1>
    <p>Updated brief: {brief}</p>
    <p>New features added!</p>
    </body>
    </html>
    """
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ App saved at {index_html_path}")

    # Auto commit to GitHub (only if repo exists)
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Round {round_number} update"], check=False)
        subprocess.run(["git", "push"], check=False)
        print("✅ Changes pushed to GitHub.")
    except Exception as e:
        print(f"⚠ Git push failed: {e}")

    # Notify evaluation URL
    if evaluation_url:
        try:
            res = requests.post(evaluation_url, json={"round": round_number})
            print(f"Evaluation POST response: {res.status_code} {res.text}")
        except Exception as e:
            print(f"⚠ Could not post to evaluation URL: {e}")

    return jsonify({"message": "Round processed", "round": round_number}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
