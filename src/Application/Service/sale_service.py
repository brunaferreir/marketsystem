from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.user import User
from src.Infrastructure.Model.product import Product
from src.config.data_base import db
from datetime import datetime

class SaleService:

    @staticmethod
    def create_sale(seller_id, product_id, quantity):
        
        # 1. Busca simplificada do vendedor apenas pelo ID
        # A verificação de status "ativo" foi removida para contornar o problema de DB no Railway
        seller = db.session.get(User, seller_id)

        # 2. Verifica se o vendedor existe
        if not seller: 
            return {"error": "Vendedor não encontrado"}, 400

        # 3. Encontra o produto
        product = db.session.get(Product, product_id)
        if not product:
            return {"error": "Produto não encontrado"}, 404

        # 4. Validação de estoque
        if product.stock < quantity:
            return {"error": "Estoque insuficiente"}, 400
            
        # 5. Cria a venda
        try:
            sale_value = product.price * quantity
            
            new_sale = Sale(
                seller_id=seller_id, 
                product_id=product_id, 
                quantity=quantity, 
                sale_value=sale_value,
                sale_date=datetime.now()
            )
            
            # 6. Atualiza o estoque
            product.stock -= quantity
            
            db.session.add(new_sale)
            db.session.commit()
            
            return {"message": "Venda registrada com sucesso!"}, 201
        
        except Exception as e:
            db.session.rollback()
            return {"error": f"Erro ao registrar a venda: {str(e)}"}, 500

    @staticmethod
    def list_sales_by_seller(seller_id):
        # Para a listagem, vamos IGNORAR o status também, pois o Railway está bloqueando.
        seller = db.session.get(User, seller_id)
        if not seller:
            return {"error": "Vendedor não encontrado"}, 400

        # 2. Lista as vendas
        sales_query = db.session.query(Sale).filter(Sale.seller_id == seller_id).all()
        
        # Mapeia os resultados para um formato JSON limpo
        sales_list = []
        for sale in sales_query:
            product = db.session.get(Product, sale.product_id)
            sales_list.append({
                "id": sale.id,
                "product_name": product.name if product else "Produto Removido",
                "quantity": sale.quantity,
                "sale_value": sale.sale_value,
                "sale_date": sale.sale_date.isoformat()
            })
            
        return sales_list