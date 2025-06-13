
# 🛠️ Checker Backend – IZAN'S LAB

Este es el backend en Flask que complementa el verificador de tarjetas de crédito desarrollado por IZAN'S LAB®. Está diseñado para funcionar como una API y ser desplegado en **Render**.

---

## 🚀 ¿Qué hace esta API?

Expone un endpoint `POST /check` que recibe una tarjeta y devuelve si es válida o no (modo demo).

```json
POST /check
{
  "number": "5523514410356141",
  "month": "09",
  "year": "2025",
  "cvv": "370"
}
```

**Respuesta esperada:**

```json
{
  "status": "LIVE",
  "message": "Tarjeta válida"
}
```

---

## 🧩 Estructura del proyecto

```
checker-backend-render/
│
├── braintree_api_server.py  # API principal con Flask
├── requirements.txt         # Librerías necesarias
├── render.yaml              # Configuración de despliegue en Render
└── README.md                # Este archivo
```

---

## ⚙️ Despliegue en Render (gratis)

1. Sube esta carpeta a GitHub
2. Ve a [https://render.com/](https://render.com/)
3. Elige **New → Web Service** y selecciona tu repo
4. Render detectará Flask y desplegará automáticamente tu API

**URL resultante (ejemplo):**  
`https://checker-backend-render.onrender.com/check`

---

## 🧠 Notas

- Este backend está en modo demo. Puedes integrar Braintree real más adelante.
- Está preparado para conectarse al frontend en Vercel.

---

👑 Desarrollado por IZAN'S LAB ® – 2025
