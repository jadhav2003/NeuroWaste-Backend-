# app.py - copy & paste this whole file
from flask import Flask, request, jsonify
import os
import json
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from your frontend

# Initialize Firebase using environment variables
firebase_key = os.getenv("FIREBASE_SERVICE_ACCOUNT")
firebase_url = os.getenv("FIREBASE_DB_URL")

if firebase_key and firebase_url:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": os.getenv("FIREBASE_DB_URL")
    })
else:
    # If env vars not present, it will still run but DB calls will fail until configured
    print("WARNING: FIREBASE_SERVICE_ACCOUNT or FIREBASE_DB_URL not set")

@app.route("/")
def home():
    return jsonify({"message": "NeuroWaste Backend Running"})

@app.route("/update", methods=["POST"])
def update_bin():
    try:
        data = request.get_json(force=True) or {}
        bin_id = data.get("bin_id")
        level = data.get("level")
        if not bin_id or level is None:
            return jsonify({"error": "bin_id and level required"}), 400
        ref = db.reference(f"bins/{bin_id}")
        ref.set({"level": level})
        return jsonify({"success": True, "bin_id": bin_id, "level": level})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/bins", methods=["GET"])
def get_bins():
    try:
        ref = db.reference("bins")
        return jsonify(ref.get() or {})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Note: keep or remove the below block — it only runs when you run python app.py locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
