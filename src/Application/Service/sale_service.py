# src/Application/Service/sale_service.py
from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.user import User
from src.Infrastructure.Model.product import Product
from src.config.data_base import db

class SaleService:

    @staticmethod
    def create_sale(seller_id, product_id, quantity):
        # verifica se seller existe e está ativo
        seller = User.query.filter_by(id=seller_id, status="ativo").first()
        if not seller:
            return {"error": "Vendedor inativo ou não encontrado"}, 400

        # verifica se o produto existe e está ativo
        product = Product.query.filter_by(id=product_id, status="ativo").first()
        if not product:
            return {"error": "Produto inativo ou não encontrado"}, 400

        # verifica se há estoque suficiente
        if product.quantity < quantity:
            return {"error": "Estoque insuficiente"}, 400

        # registra venda
        sale = Sale(
            product_id=product.id,
            seller_id=seller.id,
            quantity_sold=quantity,
            price_at_sale=product.price
        )

        # atualiza estoque
        product.quantity -= quantity

        db.session.add(sale)
        db.session.commit()

        return sale.to_dict(), 201

    @staticmethod
    def list_sales_by_seller(seller_id):
        sales = Sale.query.filter_by(seller_id=seller_id).all()
        return [s.to_dict() for s in sales]
