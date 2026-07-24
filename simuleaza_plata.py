import requests

url = "http://localhost:8000/webhook"

headers = {"Content-Type": "application/json", "Stripe-Signature": "simulat_local"}

# Payload-ul structurat conform schemei StripeWebhookPayload din main.py
payload = {
    "type": "checkout.session.completed",
    "data": {
        "object": {
            "metadata": {"order_id": "8"},
            "payment_status": "paid",
            "customer_details": {"email": "test_client@infinity.ai"},
            "amount_total": 15000,
        }
    },
}

try:
    print(f"ðŸš€ Trimitere webhook securizat catre: {url}...")
    r = requests.post(url, json=payload, headers=headers)
    print(f"[Status Server]: {r.status_code}")
    print(f"[Raspuns JSON]: {r.text}")
except Exception as e:
    print(f"âŒ Eroare la trimiterea request-ului: {e}")

