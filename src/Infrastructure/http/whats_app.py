import os
from twilio.rest import Client

def enviar_codigo_whatsapp(telefone: str, codigo: str):
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=from_number,
        body=f"Seu código de ativação é: {codigo}",
        to=f"whatsapp:{telefone}"
    )

    print(f"[Twilio] Mensagem enviada para {telefone}, SID: {message.sid}")
