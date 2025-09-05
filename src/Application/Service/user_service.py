from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db 

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