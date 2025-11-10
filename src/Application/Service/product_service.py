import sys, os
from werkzeug.utils import secure_filename


current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../../..")) 
if src_dir not in sys.path:
    sys.path.append(src_dir)


from src.Infrastructure.Model.product import Product

from src.config.data_base import db

UPLOAD_FOLDER = "uploads"

class ProductService:

    @staticmethod
    # ✅ CORREÇÃO APLICADA: Muda de 'image_file' para 'image_url'
    def create_product(user_id, name, price, quantity, status, image_url=None):
        # O image_path no Model Product agora armazena a URL da imagem (string)
        image_path = image_url 

        new_product = Product(
            name=name,
            price=price,
            quantity=quantity,
            status=status or "ativo",
            image_path=image_path, # Armazena a URL
            user_id=user_id
        )
        
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def list_products(user_id):
        # A listagem continua a mesma
        return Product.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_product_by_id(product_id, user_id):
        # A busca continua a mesma
        return Product.query.filter_by(id=product_id, user_id=user_id).first()

    @staticmethod
    def update_product(product_id, user_id, data, image_file=None):
        product = ProductService.get_product_by_id(product_id, user_id)
        if not product:
            return None

        # ⚠️ Se o Front-end enviar a URL da imagem no PUT/PATCH, a chave no 'data' deve ser a mesma
        # usada no Model (ex: 'image_path' ou 'image_url')

        for key, value in data.items():
            if hasattr(product, key) and key != "id":
                # Se 'data' inclui 'image_path' com a URL, ela é atualizada aqui
                setattr(product, key, value)

        # Esta seção de upload de arquivo está mantida caso você implemente o upload de arquivo no futuro, 
        # mas não será usada agora se você enviar apenas a URL.
        if image_file:
            os.makedirs(f"{UPLOAD_FOLDER}/{user_id}", exist_ok=True)
            filename = secure_filename(image_file.filename)
            image_path = f"{UPLOAD_FOLDER}/{user_id}/{filename}"
            image_file.save(image_path)
            product.image_path = image_path

        db.session.commit()
        return product

    @staticmethod
    def toggle_status(product_id, user_id):
        product = ProductService.get_product_by_id(product_id, user_id)
        if not product:
            return None
        product.status = "inativo" if product.status == "ativo" else "ativo"
        db.session.commit()
        return product