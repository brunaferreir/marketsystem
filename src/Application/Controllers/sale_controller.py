# EM: src/Application/Controllers/sale_controller.py

from flask import Blueprint, request, jsonify
from src.Application.Service.sale_service import SaleService
from flask_jwt_extended import jwt_required, get_jwt_identity

sale_bp = Blueprint("sale_bp", __name__, url_prefix="/api/sales")

@sale_bp.route("/", methods=["POST"])
@jwt_required()
def create_sale():
    data = request.get_json()
    seller_id_str = get_jwt_identity() # Pega o ID do token
    
    # *** AJUSTE FINAL: CONVERSÃO ROBUSTA DO ID ***
    try:
        # Tenta converter o ID para inteiro. Cobrirá se for None (TypeError) ou não-numérico (ValueError).
        seller_id = int(seller_id_str)
    except (ValueError, TypeError):
        # Se falhar, o token é inválido/ausente. Retorna 401
        return jsonify({"error": "Token inválido ou ausente. Faça login novamente."}), 401
    
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    # Chama o serviço
    response, status = SaleService.create_sale(seller_id, product_id, quantity)
    return jsonify(response), status

@sale_bp.route("/", methods=["GET"])
@jwt_required()
def list_sales():
    seller_id_str = get_jwt_identity()
    
    try:
        seller_id = int(seller_id_str)
    except (ValueError, TypeError):
        return jsonify({"error": "Token inválido ou ausente. Faça login novamente."}), 401
    
    sales = SaleService.list_sales_by_seller(seller_id)
    return jsonify(sales), 200