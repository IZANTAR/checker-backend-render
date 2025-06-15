
def check(data):
    cc = data.get("number")
    mm = data.get("month")
    yy = data.get("year")
    cvv = data.get("cvv")
    # Simulación de respuesta DIE
    return {
        "status": "DIE",
        "message": "Tarjeta rechazada (Stripe)",
        "card": cc,
        "month": mm,
        "year": yy,
        "cvv": cvv
    }
