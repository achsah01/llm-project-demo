from flask import Flask, request, jsonify
import os

app = Flask(__name__)

SECRET = "mysecret123"

@app.route("/api-endpoint", methods=["POST"])
def api_endpoint():
    data = request.get_json()
    if not data or data.get("secret") != SECRET:
        return jsonify({"status": "error", "message": "Invalid secret"}), 403

    brief = data.get("brief", "")
    print("Received brief:", brief)

    # Step 1: Create folder
    os.makedirs("generated_app", exist_ok=True)

    # Step 2: Generate HTML page
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated App</title>
    </head>
    <body>
        <h1>Auto-generated App</h1>
        <p>Brief: {brief}</p>
    </body>
    </html>
    """
    with open("generated_app/index.html", "w", encoding="utf-8") as f:
        f.write(html_code)

    print("✅ App generated successfully at ./generated_app/index.html")

    return jsonify({"status": "ok", "message": "App generated"}), 200

if __name__ == "__main__":
    app.run(debug=True)
