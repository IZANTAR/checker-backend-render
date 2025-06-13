
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import braintree

app = Flask(__name__)
CORS(app)

# Configuración de Braintree usando variables de entorno
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox if os.getenv("BT_ENVIRONMENT") == "sandbox" else braintree.Environment.Production,
        merchant_id=os.getenv("BT_MERCHANT_ID"),
        public_key=os.getenv("BT_PUBLIC_KEY"),
        private_key=os.getenv("BT_PRIVATE_KEY")
    )
)

@app.route("/check", methods=["POST"])
def check_card():
    data = request.get_json()
    cc = data.get("number")
    mm = data.get("month")
    yy = data.get("year")
    cvv = data.get("cvv")

    try:
        result = gateway.payment_method.create({
            "customer_id": "test-customer",
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

        if result.is_success:
            return jsonify({"status": "LIVE", "message": "Tarjeta válida"})
        else:
            return jsonify({"status": "DIE", "message": result.message})

    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)})

@app.route("/", methods=["GET"])
def home():
    return "IZAN'S LAB - Checker API (Braintree Ready)", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
