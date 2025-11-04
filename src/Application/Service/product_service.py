import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.Domain.product import ProductDomain
from src.config.data_base import db
from werkzeug.utils import secure_filename


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

        new_product = ProductDomain(
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
        return ProductDomain.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_product_by_id(product_id, user_id):
        return ProductDomain.query.filter_by(id=product_id, user_id=user_id).first()

    @staticmethod
    def update_product(product_id, user_id, data, image_file=None):
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
        product = ProductService.get_product_by_id(product_id, user_id)
        if not product:
            return None
        product.status = "inativo" if product.status == "ativo" else "ativo"
        db.session.commit()
        return product
