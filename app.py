from flask import Flask, request, jsonify
import os, json
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS   # add this

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

# Load Firebase from environment variables
firebase_url = os.getenv("FIREBASE_DB_URL")
firebase_key = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if not firebase_admin._apps:
    if firebase_key and firebase_url:
        cred = credentials.Certificate(json.loads(firebase_key))
        firebase_admin.initialize_app(cred, {
            'databaseURL': firebase_url
        })

@app.route("/")
def home():
    return {"message": "NeuroWaste Backend Running"}

@app.route("/update", methods=["POST"])
def update_bin():
    try:
        data = request.json
        bin_id = data.get("bin_id")
        level = data.get("level")
        if not bin_id or level is None:
            return {"error": "bin_id and level required"}, 400
        ref = db.reference(f"bins/{bin_id}")
        ref.set({"level": level})
        return {"success": True, "bin_id": bin_id, "level": level}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/bins", methods=["GET"])
def get_bins():
    try:
        ref = db.reference("bins")
        return jsonify(ref.get() or {})
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
