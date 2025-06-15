from flask import Flask, request, jsonify
from flask_cors import CORS
import braintree
import os

app = Flask(__name__)
CORS(app)

# Configuración segura con variables de entorno (ya añadidas en Render)
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get("BRAINTREE_MERCHANT_ID"),
        public_key=os.environ.get("BRAINTREE_PUBLIC_KEY"),
        private_key=os.environ.get("BRAINTREE_PRIVATE_KEY")
    )
)

@app.route('/')
def home():
    return '® IZAN’S LAB Checker Supreme ® – Backend activo en Render ✅'

@app.route('/check', methods=['POST'])
def check_card():
    data = request.get_json()
    card_number = data.get('card_number')
    expiration_month = data.get('exp_month')
    expiration_year = data.get('exp_year')
    cvv = data.get('cvv')

    try:
        result = gateway.payment_method.create({
            "customer_id": "fake_customer_id",
            "payment_method_nonce": "fake-valid-nonce",
            "credit_card": {
                "number": card_number,
                "expiration_month": expiration_month,
                "expiration_year": expiration_year,
                "cvv": cvv
            }
        })

        if result.is_success:
            return jsonify({
                "status": "live",
                "message": "Estado: Viva – Saldo desconocido"
            }), 200
        else:
            return jsonify({
                "status": "dead",
                "message": "Tarjeta rechazada – Estado: Muerta"
            }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error en la validación: {str(e)}"
        }), 500

# Bloque para ejecución correcta en Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
