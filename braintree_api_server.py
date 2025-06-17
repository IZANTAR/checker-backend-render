from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def obtener_datos_bin(bin_number):
    try:
        url = f"https://bincheck.io/details/{bin_number}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        info = {}

        def extraer(dato):
            elemento = soup.find("th", string=dato)
            if elemento and elemento.find_next_sibling("td"):
                return elemento.find_next_sibling("td").text.strip()
            return ""

        info["banco"] = extraer("Bank")
        info["pais"] = extraer("Country")
        info["marca"] = extraer("Brand")
        info["nivel"] = extraer("Level")
        info["tipo"] = extraer("Type")
        bandera = soup.find("img", {"class": "country-flag"})
        info["bandera"] = bandera["src"] if bandera else ""
        return info
    except Exception:
        return {}

@app.route("/check", methods=["POST"])
def verificar_tarjeta():
    data = request.get_json()
    card = data.get("number", "")
    month = data.get("month", "")
    year = data.get("year", "")
    cvv = data.get("cvv", "")
    bin_number = card[:6]

    if card.startswith("4") or card.startswith("5"):
        bin_info = obtener_datos_bin(bin_number)
        resultado = {
            "status": "LIVE",
            "card": card,
            "month": month,
            "year": year,
            "cvv": cvv,
            "bin": bin_info
        }
    else:
        resultado = {
            "status": "DIE",
            "card": card,
            "month": month,
            "year": year,
            "cvv": cvv,
            "bin": {}
        }

    return jsonify(resultado)

if __name__ == "__main__":
    print("Server running")
    app.run(host="0.0.0.0", port=10000)
