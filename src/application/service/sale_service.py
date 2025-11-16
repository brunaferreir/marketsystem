from src.infrastructure.model.product_model import Product
from src.infrastructure.model.sale_model import Sale
from src.infrastructure.model.user_model import User
from src.config.data_base import db
from datetime import datetime, timedelta


def br_time():
    """Retorna a data e hora de Brasília (UTC-3)"""
    return datetime.utcnow() - timedelta(hours=3)


class SaleService:
    @staticmethod
    def register_sale(product_id, quantity, seller_id):
        try:
            seller = User.query.get(seller_id)
            if not seller or seller.status != "active":
                return None, "Vendedor não autorizado ou inativo.", 403

            product = Product.query.get(product_id)
            if not product:
                return None, "Produto não encontrado.", 404

            if product.status != "active":
                return None, "Produto inativo não pode ser vendido.", 400

            if product.quantity < quantity:
                return None, f"Estoque insuficiente. Quantidade disponível: {product.quantity}", 409

            # Atualiza o estoque
            product.quantity -= quantity

            # Cria a venda com hora de Brasília
            new_sale = Sale(
                product_id=product_id,
                user_id=seller_id,
                quantity=quantity,
                price_at_sale=product.price,
                created_at=br_time()
            )

            db.session.add(new_sale)
            db.session.commit()

            return new_sale, None, 201

        except Exception as e:
            db.session.rollback()
            return None, f"Erro ao registrar venda: {str(e)}", 500

    @staticmethod
    def get_sales(seller_id=None):
        """
        Retorna todas as vendas com nome do produto, preço e data/hora.
        """
        try:
            query = db.session.query(Sale, Product).join(Product, Sale.product_id == Product.id)

            if seller_id:
                query = query.filter(Sale.user_id == seller_id)

            sales = query.all()

            sales_data = []
            for sale, product in sales:
                sales_data.append({
                    "product_id": sale.product_id,
                    "product_name": product.name,
                    "price": float(sale.price_at_sale),
                    "date": sale.created_at.isoformat() if sale.created_at else None
                })

            return sales_data

        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erro ao buscar vendas: {str(e)}")
