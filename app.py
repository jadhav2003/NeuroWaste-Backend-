import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# -------------------- FIREBASE INITIALIZATION --------------------
# Path to your JSON service account file
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
DATABASE_URL = "https://neurowaste-625d1-default-rtdb.asia-southeast1.firebasedatabase.app"

try:
    # Load credentials
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)

    # Initialize Firebase app only once
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
    print("✅ Firebase initialized successfully")

    # Test write
    ref = db.reference("/")
    ref.set({"status": "connected"})
    print("🔥 Test data written successfully")

except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")

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
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
