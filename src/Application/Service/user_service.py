from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 
import random
from src.Infrastructure.http.whats_app import enviar_codigo_whatsapp
from src.Infrastructure.Model.activation_code import ActivationCode


class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password, status):
        new_user = UserDomain(name, cnpj, email, celular, password, status)
        user = User(name=new_user.name, 
                     cnpj=new_user.cnpj, 
                     email=new_user.email,
                     celular= new_user.celular,
                     password=new_user.password,
                     status=new_user.status)        
        db.session.add(user)
        db.session.commit()
        return user

#AQUI------------------------------------    
    @staticmethod
    def get_user(user_id=None):
        if user_id:
            return db.session.get(User, user_id)
        # else:
        #     return db.session.query(User).all()

    #AQUI------------------------------------  PUT ATUALIZA 1 USUARIO
    @staticmethod
    def update_user(user_id, data):
        user = db.session.get(User, user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None    
    
    # AQUI------------------------------------ MÉTODO PARA AUTENTICAR O USUÁRIO
    @staticmethod
    def authenticate_user(email, password):
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.password == password:
            return user
        return None


    # AQUI------------------------------------ CADASTRAR VENDEDOR + ENVIAR CÓDIGO
    @staticmethod
    def create_seller(name, cnpj, email, celular, password):
        user = User(
            name=name,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=password,
            status="inactive"  # começa inativo
        )
        db.session.add(user)
        db.session.commit()

        # gera código de 4 dígitos
        codigo = str(random.randint(1000, 9999))
        enviar_codigo_whatsapp(celular, codigo)

        activation = ActivationCode(code=codigo, user_id=user.id)
        db.session.add(activation)
        db.session.commit()

        return {"message": "Usuário cadastrado. Código enviado por WhatsApp."}

    # AQUI------------------------------------ ATIVAR VENDEDOR COM CÓDIGO
    @staticmethod
    def activate_seller(celular, codigo):
        user = db.session.query(User).filter_by(celular=celular).first()
        if not user:
            return {"error": "Usuário não encontrado"}

        activation = db.session.query(ActivationCode).filter_by(
            user_id=user.id, code=codigo, used=False
        ).first()
        if not activation:
            return {"error": "Código inválido ou já usado"}

        activation.used = True
        user.status = "active"
        db.session.commit()

        return {"message": "Usuário ativado com sucesso!"}

    # AQUI------------------------------------ LOGIN (só se ativo)
    @staticmethod
    def login_user(email, password):
        user = db.session.query(User).filter_by(email=email, password=password).first()
        if not user:
            return {"error": "Credenciais inválidas"}
        if user.status != "active":
            return {"error": "Usuário inativo. Ative primeiro."}
        return {"message": "Login realizado com sucesso!"}

 