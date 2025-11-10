from src.config.data_base import db
from datetime import datetime
# Importar db.Text (opcionalmente) ou garantir que seja usado
from sqlalchemy import Text 

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="ativo")  # "ativo" ou "inativo"
    
    # ✅ CORREÇÃO: Alterar de db.String(255) para db.Text para suportar URLs longas
    image_path = db.Column(db.Text) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("products", lazy=True))



    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price), 
            "quantity": int(self.quantity), 
            "status": self.status,
            "image_path": self.image_path,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
        }