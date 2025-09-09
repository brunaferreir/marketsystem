from src.config.data_base import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    celular = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    # Relacionamento com a tabela de códigos de ativação
    activation_codes = db.relationship(
        'ActivationCode',
        back_populates='user',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cnpj': self.cnpj,
            'email': self.email,
            'celular': self.celular,
            'status': self.status
        }