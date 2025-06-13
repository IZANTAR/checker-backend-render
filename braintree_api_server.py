
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/check", methods=["POST"])
def check_card():
    data = request.get_json()
    cc = data.get("number")
    mm = data.get("month")
    yy = data.get("year")
    cvv = data.get("cvv")

    # Simulación de verificación real
    if cc and len(cc) >= 13:
        return jsonify({"status": "LIVE", "message": "Tarjeta válida"})
    return jsonify({"status": "DIE", "message": "Rechazada"})

@app.route("/", methods=["GET"])
def home():
    return "IZAN'S LAB - Checker API (Render Ready)", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
