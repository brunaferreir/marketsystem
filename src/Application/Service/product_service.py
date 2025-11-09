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
    def create_product(user_id, name, price, quantity, status, image_file=None):
        image_path = None

        if image_file:
            os.makedirs(f"{UPLOAD_FOLDER}/{user_id}", exist_ok=True)
            filename = secure_filename(image_file.filename)
            image_path = f"{UPLOAD_FOLDER}/{user_id}/{filename}"
            image_file.save(image_path)

        # ⚠️ CORREÇÃO DE MAPEAMENTO: Use a classe MAPEADA (Product) em vez de ProductDomain
        new_product = Product(
            name=name,
            price=price,
            quantity=quantity,
            status=status or "ativo",
            image_path=image_path,
            user_id=user_id
        )
        
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def list_products(user_id):
        # ⚠️ CORREÇÃO DE MAPEAMENTO: Use a classe MAPEADA (Product)
        return Product.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_product_by_id(product_id, user_id):
        # ⚠️ CORREÇÃO DE MAPEAMENTO: Use a classe MAPEADA (Product)
        return Product.query.filter_by(id=product_id, user_id=user_id).first()

    @staticmethod
    def update_product(product_id, user_id, data, image_file=None):
        # Esta função usa o resultado de get_product_by_id, que agora retorna um objeto Product mapeado
        product = ProductService.get_product_by_id(product_id, user_id)
        if not product:
            return None

        for key, value in data.items():
            if hasattr(product, key) and key != "id":
                setattr(product, key, value)

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
        # Esta função usa o resultado de get_product_by_id
        product = ProductService.get_product_by_id(product_id, user_id)
        if not product:
            return None
        product.status = "inativo" if product.status == "ativo" else "ativo"
        db.session.commit()
        return product