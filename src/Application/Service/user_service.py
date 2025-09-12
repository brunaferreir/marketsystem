from flask_jwt_extended import create_access_token
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
import random
from src.Infrastructure.http.whats_app import enviar_codigo_whatsapp
from src.Infrastructure.Model.activation_code import ActivationCode

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password):
        new_user = UserDomain(
            name=name,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=password, 
            status="inactive"
        )
        
        user = User(
            name=new_user.name, 
            cnpj=new_user.cnpj, 
            email=new_user.email,
            celular=new_user.celular,
            password=new_user.password,
            status=new_user.status
        )
        
        db.session.add(user)
        db.session.commit()
        return user


    @staticmethod
    def get_seller_by_id(user_id=None):
        if user_id:
            return db.session.get(User, user_id)
        
    @staticmethod
    def update_user(user_id, data):
        user = db.session.get(User, user_id)
        if user:
            if 'password' in data:
                data['password'] = data['password']

            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None

    @staticmethod
    def authenticate_user(email, password):
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.password == password:
            return user
        return None

    #---------------------- CADASTRAR VENDEDOR + ENVIAR CÓDIGO
    @staticmethod
    def create_seller(name, cnpj, email, celular, password):
        try:
            user = UserService.create_user(name, cnpj, email, celular, password)
            
            codigo = str(random.randint(1000, 9999))
            
            enviar_codigo_whatsapp(celular, codigo)

            activation = ActivationCode(code=codigo, user_id=user.id)
            db.session.add(activation)
            db.session.commit()

            return {"message": "Usuário cadastrado. Código de ativação enviado por WhatsApp."}
        except Exception as e:
            return {"error": f"Erro ao criar vendedor: {e}"}

    #---------------------- ATIVAR VENDEDOR COM CÓDIGO
    @staticmethod
    def activate_seller(celular, codigo):
        user = db.session.query(User).filter_by(celular=celular).first()
        if not user:
            return {"error": "Usuário não encontrado."}

        activation = db.session.query(ActivationCode).filter_by(
            user_id=user.id, code=codigo, used=False
        ).first()
        if not activation:
            return {"error": "Código inválido ou já usado."}

        activation.used = True
        user.status = "active"
        db.session.commit()

        return {"message": "Usuário ativado com sucesso!"}
        
    #---------------------- LOGIN (só se ativo)
    @staticmethod
    def login_seller(email, password):
        user = UserService.authenticate_user(email, password)
        if not user:
            return {"error": "Credenciais inválidas."}

        if user.status != "active":
            return {"error": "Usuário inativo. Ative primeiro."}

        # Gera o token de acesso
        token = create_access_token(identity=user.id)
        return {"token": token, "message": "Login realizado com sucesso!"}
    
    @staticmethod
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def inacttivate_user(user_id):
        user = db.session.get(User, user_id)
        if user:
            user.status = "inactive"
            db.session.commit()
            return user
        return None
