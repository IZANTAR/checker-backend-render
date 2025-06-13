
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import braintree
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox if os.getenv("BT_ENVIRONMENT") == "sandbox" else braintree.Environment.Production,
        merchant_id=os.getenv("BT_MERCHANT_ID"),
        public_key=os.getenv("BT_PUBLIC_KEY"),
        private_key=os.getenv("BT_PRIVATE_KEY")
    )
)

def obtener_info_bin(bin_code):
    try:
        r = requests.get(f"https://bincheck.io/details/{bin_code}", timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        tabla = soup.find("table")
        datos = {row.th.text.strip().lower(): row.td.text.strip() for row in tabla.find_all("tr")}
        pais = datos.get("country", "")
        marca = datos.get("scheme", "")
        tipo = datos.get("type", "")
        nivel = datos.get("brand", "")
        banco = datos.get("bank", "")
        return {
            "pais": pais,
            "marca": marca,
            "tipo": tipo,
            "nivel": nivel,
            "banco": banco,
            "bandera": f"https://flagsapi.com/{pais[:2].upper()}/flat/64.png" if len(pais) >= 2 else ""
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/check", methods=["POST"])
def check_card():
    data = request.get_json()
    cc = data.get("number")
    mm = data.get("month")
    yy = data.get("year")
    cvv = data.get("cvv")

    bin_code = cc[:8] if len(cc) >= 8 else cc[:6]
    bin_info = obtener_info_bin(bin_code)

    try:
        result = gateway.payment_method.create({
            "customer_id": "izan-checker",
            "payment_method_nonce": "fake-valid-nonce",
            "credit_card": {
                "number": cc,
                "expiration_month": mm,
                "expiration_year": yy,
                "cvv": cvv,
                "options": {
                    "verify_card": True
                }
            }
        })

        estado = "LIVE" if result.is_success else "DIE"
        mensaje = "Tarjeta válida" if result.is_success else result.message

        return jsonify({
            "status": estado,
            "message": mensaje,
            "card": cc,
            "month": mm,
            "year": yy,
            "cvv": cvv,
            "bin": bin_info
        })

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e),
            "card": cc,
            "month": mm,
            "year": yy,
            "cvv": cvv,
            "bin": bin_info
        })

@app.route("/", methods=["GET"])
def home():
    return "IZAN'S LAB - Checker API (BIN + Braintree)", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
