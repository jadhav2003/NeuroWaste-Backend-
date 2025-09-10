import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Load Firebase credentials from serviceAccountKey.json (must be in repo or env var)
firebase_key = os.getenv("FIREBASE_SERVICE_ACCOUNT")
firebase_url = os.getenv("FIREBASE_DB_URL")

if firebase_key and firebase_url:
    try:
        # Local service account file
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": firebase_url
        })
        print("✅ Firebase initialized successfully")
    except Exception as e:
        print(f"⚠️ Firebase initialization failed: {e}")
else:
    # Warn but don’t crash
    print("⚠️ WARNING: FIREBASE_SERVICE_ACCOUNT or FIREBASE_DB_URL not set")


# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return jsonify({"message": "NeuroWaste API is running 🚀"})


@app.route("/update", methods=["POST"])
def update_bin():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    bin_id = data.get("bin_id")
    level = data.get("level")

    if not bin_id or level is None:
        return jsonify({"error": "bin_id and level are required"}), 400

    try:
        ref = db.reference(f"/bins/{bin_id}")
        ref.set({"level": level})
        return jsonify({"success": True, "bin_id": bin_id, "level": level})
    except Exception as e:
        return jsonify({"error": f"Failed to update Firebase: {e}"}), 500


@app.route("/bins", methods=["GET"])
def get_bins():
    try:
        ref = db.reference("/bins")
        bins = ref.get()
        return jsonify(bins if bins else {})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch bins: {e}"}), 500


# -------------------- ENTRYPOINT --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
