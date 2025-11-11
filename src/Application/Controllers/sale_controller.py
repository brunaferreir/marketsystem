from flask import Blueprint, request, jsonify
from src.Application.Service.sale_service import SaleService
from flask_jwt_extended import jwt_required, get_jwt_identity

sale_bp = Blueprint("sale_bp", __name__, url_prefix="/api/sales")

@sale_bp.route("/", methods=["POST"])
@jwt_required()
def create_sale():
    seller_id_str = get_jwt_identity()
    
    # *** ESTE TRECHO É O SEU "PRINT()" ***
    try:
        seller_id = int(seller_id_str)
        # Se for bem-sucedido, retorna 200 e o ID. SEU ID DEVE ESTAR AQUI!
        return jsonify({
            "DIAGNOSTICO_SUCESSO": "Token Decodificado Corretamente",
            "SELLER_ID_DECODIFICADO": seller_id,
            "TIPO_DECODIFICADO": str(type(seller_id))
        }), 200
        
    except (ValueError, TypeError):
        # Se falhar (ID for None, por exemplo), retorna 401
        return jsonify({
            "DIAGNOSTICO_FALHA": "Token não decodificou a identidade (ID)",
            "VALOR_BRUTO": str(seller_id_str)
        }), 401
    # *** FIM DO DIAGNÓSTICO TEMPORÁRIO ***

# A rota list_sales não precisa ser alterada.
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