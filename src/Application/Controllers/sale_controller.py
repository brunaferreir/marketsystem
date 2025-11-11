from flask import Blueprint, request, jsonify
from src.Application.Service.sale_service import SaleService
from flask_jwt_extended import jwt_required, get_jwt_identity

sale_bp = Blueprint("sale_bp", __name__, url_prefix="/api/sales")

@sale_bp.route("/", methods=["POST"])
@jwt_required()
def create_sale():
    data = request.get_json()
    seller_id_str = get_jwt_identity() # Pega o ID do token (ex: "2" como string)
    
    # 🚨 NOVO LOG DE DIAGNÓSTICO
    print(f"--- DIAGNÓSTICO DE VENDA ---")
    print(f"Token Identity (String): {seller_id_str}") # O que o get_jwt_identity() retornou
    
    # *** CORREÇÃO: CONVERTE ID PARA INTEIRO (INT) ANTES DE USAR NA BUSCA ***
    # Adicionando TypeError para cobrir caso get_jwt_identity() retorne None
    try:
        # Tenta converter para inteiro. Falha se for None ou não-numérico.
        seller_id = int(seller_id_str)
        print(f"Seller ID (Integer): {seller_id}") # ID usado na busca
    except (ValueError, TypeError):
        # Se o token estiver corrompido ou for None, retorna erro 401
        print(f"ERRO: Identity do token inválida ou None: {seller_id_str}")
        return jsonify({"error": "Token inválido ou corrompido"}), 401
    
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    # Chama o serviço, passando o seller_id AGORA como inteiro (int)
    response, status = SaleService.create_sale(seller_id, product_id, quantity)
    return jsonify(response), status

@sale_bp.route("/", methods=["GET"])
@jwt_required()
def list_sales():
    seller_id_str = get_jwt_identity()
    
    try:
        seller_id = int(seller_id_str)
    except (ValueError, TypeError): # Adicionei TypeError aqui também
        return jsonify({"error": "Token inválido ou corrompido"}), 401
    
    sales = SaleService.list_sales_by_seller(seller_id)
    return jsonify(sales), 200