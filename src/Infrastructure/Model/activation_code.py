from src.config.data_base import db
from sqlalchemy.orm import relationship

class ActivationCode(db.Model):
    __tablename__ = 'activation_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    used = db.Column(db.Boolean, default=False)

    user = db.relationship(
        'User',
        back_populates='activation_codes'
    )
    
    def __repr__(self):
        return f'<ActivationCode {self.code}>'