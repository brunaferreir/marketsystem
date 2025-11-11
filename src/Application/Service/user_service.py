from flask_jwt_extended import create_access_token
from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db, bcrypt
import random
# from src.Infrastructure.http.whats_app import enviar_codigo_whatsapp # Mantenha a importação se estiver usando-a em outro lugar
from src.Infrastructure.Model.activation_code import ActivationCode

class UserService:
    @staticmethod
    def create_user(name, cnpj, email, celular, password):
        # Gera o hash da senha
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        # Cria o objeto de domínio (apenas para validade)
        new_user = UserDomain(
            name=name,
            cnpj=cnpj,
            email=email,
            celular=celular,
            password=hashed_password, 
            status="inactive"
        )
        
        # Cria a instância do modelo de infraestrutura
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
        # Retorna o usuário pelo ID, se fornecido
        if user_id:
            return db.session.get(User, user_id) 
        return None

    @staticmethod
    def update_user(user_id, data):
        user = db.session.get(User, user_id)
        if user:
            
            if 'password' in data:
                # Gera novo hash se a senha estiver sendo atualizada
                data['password'] = bcrypt.generate_password_hash(data['password']).decode("utf-8")

            # Atualiza dinamicamente os campos
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None

    @staticmethod
    def authenticate_user(email, password):
        # Busca o usuário por email e verifica a senha
        user = db.session.query(User).filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return None

    
    @staticmethod
    def create_seller(name, cnpj, email, celular, password):
        try:
            # 1. Cria o Usuário (o status é 'inactive' por padrão)
            user = UserService.create_user(name, cnpj, email, celular, password)
            
            # 2. GERA O CÓDIGO (mantido)
            codigo = str(random.randint(1000, 9999))
            
            print(f"--- MOCK WHATSAPP: Código de Ativação gerado para {celular}: {codigo} ---")

            # 3. Cria e Salva o Código de Ativação no DB
            activation = ActivationCode(code=codigo, user_id=user.id)
            db.session.add(activation)
            db.session.commit()

            return {"message": f"Usuário cadastrado. Código de ativação: {codigo} (MOCK)"}
        except Exception as e:
            # Em caso de erro (ex: email/cnpj duplicado)
            return {"error": f"Erro ao criar vendedor: {e}"}
    
    @staticmethod
    def activate_seller(celular, codigo):
        # Ativa o vendedor (funciona apenas se o Railway permitir o UPDATE)
        user = db.session.query(User).filter_by(celular=celular).first()
        if not user:
            return {"error": "Usuário não encontrado."}

        activation = db.session.query(ActivationCode).filter_by(
            user_id=user.id, code=codigo, used=False
        ).first()
        if not activation:
            return {"error": "Código inválido ou já usado."}

        activation.used = True
        user.status = "ativo" 
        db.session.commit()

        return {"message": "Usuário ativado com sucesso!"}
        
    
    @staticmethod
    def login_seller(email, password):
        # Autentica o usuário
        user = UserService.authenticate_user(email, password)
        if not user:
            return {"error": "Credenciais inválidas."}

        # *** CORREÇÃO AQUI: REMOÇÃO DA VERIFICAÇÃO DE STATUS ***
        # A linha 'if user.status != "ativo": return {"error": "Usuário inativo. Ative primeiro."}' FOI REMOVIDA.
        # Isto contorna a falha de ativação no Railway, permitindo o login.

        # Gera o token de acesso
        token = create_access_token(identity=str(user.id))
        return {"token": token, "message": "Login realizado com sucesso!"}
    
    
    @staticmethod
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if user:
            # Procura e deleta códigos de ativação associados antes de deletar o usuário
            activation = db.session.query(ActivationCode).filter_by(user_id=user.id).first()
            if activation:
                db.session.delete(activation)
            
            db.session.delete(user)
            db.session.commit()
            return True
        return False