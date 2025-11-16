import os
import random
from twilio.rest import Client

class WhatsApp:
    def __init__(self, account_sid, auth_token, from_number):
        if not all([account_sid, auth_token, from_number]):
            raise ValueError("As credenciais do Twilio (account_sid, auth_token, from_number) são necessárias.")
        
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_message(self, to_number, text):
        message = self.client.messages.create(
            from_=self.from_number,
            body=text,
            to=to_number
        )
        print("Mensagem enviada! SID:", message.sid)
        return message.sid

    def send_code(self, to_number):
        code = random.randint(1000, 9999)
        text = f"Seu código de verificação é: {code}"
        self.send_message(to_number, text)
        return code

if __name__ == "__main__":
    # Para teste local, carregar as variáveis aqui
    from dotenv import load_dotenv
    load_dotenv()
    
    test_sid = os.getenv("TWILIO_ACCOUNT_SID")
    test_token = os.getenv("TWILIO_AUTH_TOKEN")
    test_from = os.getenv("FROM_NUMBER")
    to_number = 'whatsapp:+5511999999999' # Substitua pelo seu número de teste
    whatsapp = WhatsApp(test_sid, test_token, test_from)
    codigo = whatsapp.send_code(to_number)
    print("Código enviado:", codigo)
