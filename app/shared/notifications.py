import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client


def send_order_email(to_email: str, order_id: int, total_amount: float):
    """Trimite email de confirmare clientului prin SendGrid."""
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL")

    # Daca nu avem chei reale inca, doar logam actiunea ca sa nu crape backend-ul
    if not api_key or api_key.startswith("SG.your"):
        print(
            f"[MOCK EMAIL] Trimitere confirmare pentru Comanda #{order_id} catre {to_email}"
        )
        return

    try:
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=f"Confirmare Comanda #{order_id} - Light Infinity AI",
            html_content=f"<strong>Va multumim!</strong> Comanda dumneavoastra in valoare de {total_amount} RON a fost inregistrata.",
        )
        sg = SendGridAPIClient(api_key)
        sg.send(message)
        print(f"[SendGrid] Email trimis cu succes pentru comanda #{order_id}")
    except Exception as e:
        print(f"[SendGrid ERROR] Esec la trimitere email: {e}")


def check_and_send_stock_sms(material_name: str, current_stock: float):
    """Trimite alerta SMS prin Twilio daca stocul de ceara scade sub 0 kg."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or account_sid.startswith("ACyour"):
        if current_stock < 0:
            print(
                f"[MOCK SMS] ALERTÄ‚: Stocul pentru '{material_name}' este critic: {current_stock} kg!"
            )
        return

    if current_stock < 0:
        try:
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=f"ðŸš¨ ALERTÄ‚ INVENTAR ERP: Stocul pentru '{material_name}' a scazut sub pragul critic! Stoc actual: {current_stock} kg.",
                from_=os.getenv("TWILIO_PHONE_NUMBER"),
                to=os.getenv("ADMIN_PHONE_NUMBER"),
            )
            print("[Twilio] SMS de alerta stoc trimis administratorului.")
        except Exception as e:
            print(f"[Twilio ERROR] Esec la trimitere SMS: {e}")

