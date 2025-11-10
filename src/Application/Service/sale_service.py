# Em src/Application/Service/sale_service.py
from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.user import User
from src.Infrastructure.Model.product import Product
from src.config.data_base import db

class SaleService:

    @staticmethod
    def create_sale(seller_id, product_id, quantity):
        
        # 1. Busca o seller. O status DEVE ser "ativo" (em português, minúsculo)
        seller = db.session.query(User).filter(
            User.id == seller_id, 
            User.status == "ativo" # <--- CORREÇÃO CRÍTICA AQUI: Mudado de "active" para "ativo"
        ).first()

        if not seller: 
            # Este erro é retornado porque o status no BD não batia com o código
            return {"error": "Vendedor inativo ou não encontrado"}, 400 

        # 2. verifica se o produto existe, está ativo e tem estoque
        product = Product.query.filter_by(id=product_id, status="ativo").first() 
        if not product:
            return {"error": "Produto inativo ou não encontrado"}, 400
        
        if product.quantity < quantity:
            return {"error": "Estoque insuficiente para a venda"}, 400

        # 3. registra venda
        sale = Sale(
            product_id=product.id,
            seller_id=seller.id,
            quantity_sold=quantity,
            price_at_sale=product.price
        )

        # 4. atualiza estoque
        product.quantity -= quantity

        db.session.add(sale)
        db.session.commit()

        return sale.to_dict(), 201

    @staticmethod
    def list_sales_by_seller(seller_id):
        sales = Sale.query.filter_by(seller_id=seller_id).all()
        return [s.to_dict() for s in sales]