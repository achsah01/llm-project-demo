from flask import Flask, request, jsonify
import os, json, datetime
from pathlib import Path

app = Flask(__name__)
generated_folder = Path("generated_app")
generated_folder.mkdir(exist_ok=True)

@app.route("/api-endpoint", methods=["POST"])
def api_endpoint():
    data = request.get_json()
    print(f"Received request - Task: {data.get('task')}, Round: {data.get('round')}")
    
    # Generate a simple HTML app
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auto-generated App</title>
    </head>
    <body>
        <h1>Auto-generated App - Round {data.get('round')}</h1>
        <p>Updated brief: {data.get('brief')}</p>
        {"<p>New features added!</p>" if data.get('round')==2 else ""}
    </body>
    </html>
    """
    
    file_path = generated_folder / "index.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ App saved at {file_path}")
    
    # Return HTTP 200
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
