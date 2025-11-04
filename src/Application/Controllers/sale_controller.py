# src/Application/Controllers/sale_controller.py
from flask import Blueprint, request, jsonify
from src.Application.Service.sale_service import SaleService
from flask_jwt_extended import jwt_required, get_jwt_identity

sale_bp = Blueprint("sale_bp", __name__, url_prefix="/api/sales")

@sale_bp.route("/", methods=["POST"])
@jwt_required()
def create_sale():
    data = request.get_json()
    seller_id = get_jwt_identity()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    response, status = SaleService.create_sale(seller_id, product_id, quantity)
    return jsonify(response), status

@sale_bp.route("/", methods=["GET"])
@jwt_required()
def list_sales():
    seller_id = get_jwt_identity()
    sales = SaleService.list_sales_by_seller(seller_id)
    return jsonify(sales), 200
