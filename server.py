from flask import Flask, request, jsonify
import os
from pathlib import Path

app = Flask(__name__)
generated_folder = Path("generated_app")
generated_folder.mkdir(exist_ok=True)

@app.route("/api-endpoint", methods=["POST"])
def api_endpoint():
    data = request.get_json()
    task = data.get("task")
    round_num = data.get("round")
    brief = data.get("brief")
    print(f"Received request - Task: {task}, Round: {round_num}")
    
    # Auto-generate index.html content
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Auto-generated App</title>
</head>
<body>
    <h1>Auto-generated App - Round {round_num}</h1>
    <p>Updated brief: {brief}</p>
    {"<p>New features added!</p>" if round_num==2 else ""}
</body>
</html>
"""
    file_path = generated_folder / "index.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ App saved at {file_path}")

    # Simulate evaluation POST
    evaluation_url = data.get("evaluation_url")
    if evaluation_url and evaluation_url.startswith("http"):
        print(f"✅ Would POST evaluation data to: {evaluation_url}")
    else:
        print("⚠️ Invalid evaluation_url provided")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
