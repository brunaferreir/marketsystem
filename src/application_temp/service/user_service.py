from src.domain.user import UserDomain
from src.infrastructure.model.user_model import User
from src.config.data_base import db , bcrypt
from src.infrastructure.http.whats_app import WhatsApp
import os
import random

class UserService:
    @staticmethod
    def create_user(name, email, password, cnpj, number):

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = UserDomain(name, email, hashed_password, cnpj, number)
        
        whatsapp_number = f"whatsapp:{number}"

        # Carrega as credenciais do ambiente e instancia o serviço
        '''account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("FROM_NUMBER")

        whats_app_service = WhatsApp(account_sid, auth_token, from_number)
        code = whats_app_service.send_code(to_number=whatsapp_number)'''
        
        code = random.randint(1000, 9999)

        user = User(name=new_user.name, email=new_user.email, password=new_user.password, cnpj=new_user.cnpj, number=new_user.number, code = code)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user(idUser):
        user = User.query.get(idUser)
        if not user:
            return None
        return user

    
    @staticmethod
    def update_user(idUser, new_data):
        user = User.query.get(idUser)
        if not user:
            return None

        allowed_fields = ['name', 'email', 'password', 'cnpj', 'number']

        for field in allowed_fields:
            if field in new_data and new_data[field] not in [None, ""]:
                if field == "password":
                    setattr(user, field, bcrypt.generate_password_hash(new_data[field]).decode("utf-8"))
                else:
                    setattr(user, field, new_data[field])

        db.session.commit()
        return user
    
    @staticmethod
    def inativar_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        user.status = "inactive"
        db.session.commit()
        return user

    @staticmethod
    def ativar_user(number,code):
        user = User.query.filter_by(number=number).first()
        if not user:
            return None, "Usuário não encontrado"

        if user.code != code:
            return None, "Código inválido"

        user.status = "active"
        db.session.commit()
        return user , None  

    @staticmethod
    def autenticacao(email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            return None, "Usuário não encontrado"

        if not bcrypt.check_password_hash(user.password, password):
            return None, "Senha incorreta"

        if user.status != "active":
            return None, "Usuário ainda não ativado"

        return user, None
