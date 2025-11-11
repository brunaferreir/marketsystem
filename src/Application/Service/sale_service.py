from src.Infrastructure.Model.sale import Sale
from src.Infrastructure.Model.user import User
from src.Infrastructure.Model.product import Product
from src.config.data_base import db
from datetime import datetime

class SaleService:

    @staticmethod
    def create_sale(seller_id, product_id, quantity):
        
        # 1. Busca simplificada do vendedor apenas pelo ID
        # A verificação do status 'ativo' agora é feita no código Python
        seller = db.session.query(User).filter(
            User.id == seller_id
        ).first()

        # Verifica se o vendedor existe e se está ATIVO (status 'ativo' em minúsculas)
        if not seller or seller.status != "ativo": 
            return {"error": "Vendedor inativo ou não encontrado"}, 400

        # 2. Encontra o produto
        product = db.session.get(Product, product_id)
        if not product:
            return {"error": "Produto não encontrado"}, 404

        # 3. Validação de estoque
        if product.stock < quantity:
            return {"error": "Estoque insuficiente"}, 400
            
        # 4. Cria a venda
        sale_value = product.price * quantity
        
        new_sale = Sale(
            seller_id=seller_id, 
            product_id=product_id, 
            quantity=quantity, 
            sale_value=sale_value,
            sale_date=datetime.now()
        )
        
        # 5. Atualiza o estoque
        product.stock -= quantity
        
        db.session.add(new_sale)
        db.session.commit()
        
        return {"message": "Venda registrada com sucesso!"}, 201

    @staticmethod
    def list_sales_by_seller(seller_id):
        # 1. Verifica o vendedor
        seller = db.session.get(User, seller_id)
        if not seller or seller.status != "ativo":
            return {"error": "Vendedor inativo ou não encontrado"}, 400

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