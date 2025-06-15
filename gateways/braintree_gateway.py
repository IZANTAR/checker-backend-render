
def check(data):
    cc = data.get("number")
    mm = data.get("month")
    yy = data.get("year")
    cvv = data.get("cvv")
    # Simulación de respuesta LIVE
    return {
        "status": "LIVE",
        "message": "Tarjeta válida (Braintree)",
        "card": cc,
        "month": mm,
        "year": yy,
        "cvv": cvv
    }
