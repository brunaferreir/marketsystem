from src.domain.product import ProductDomain
from src.infrastructure.model.product_model import Product
from src.config.data_base import db

class ProductService:
  @staticmethod
  def create_product(name, price, quantity, status, image_url, seller_id):
    new_product = ProductDomain(name, price, quantity, status, image_url, seller_id)
    
    product = Product(
        name=new_product.name,
        price=new_product.price,
        quantity=new_product.quantity,
        status=new_product.status,
        image_url=new_product.image_url,
        seller_id=new_product.seller_id
    )

    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)  # garante que o ID recém-criado seja carregado

    return product

         
  @staticmethod
  def get_products(seller_id):
    products = Product.query.filter_by(seller_id=seller_id).all()
    if not products:
      return None
    return products
    
  @staticmethod
  def get_product_id(id):
    product = Product.query.get(id)
    return product
  
  @staticmethod
  def update_product(product_id, new_data):
    product = Product.query.get(product_id)
    if not product:
        return None

    allowed_fields = ['name', 'price', 'quantity', 'status', 'image_url']
    
    for field, value in new_data.items():
        if field in allowed_fields and value is not None:
            setattr(product, field, value)
            
    db.session.commit()
    return product

  @staticmethod
  def inativar_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return None
    product.status = "inactive"
    db.session.commit()
    return product