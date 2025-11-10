import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from src.Application.Service.product_service import ProductService

product_bp = Blueprint("product_bp", __name__, url_prefix="/api/products")


UPLOAD_FOLDER = "uploads"

@product_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    """
    Cria um novo produto vinculado ao usuário autenticado.
    """
    user_id = get_jwt_identity()
    
   
    data = request.json 
    
    
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")
    status = data.get("status", "ativo")
    image_url = data.get("image") 

  
    
    if not all([name, price, quantity]):
        return jsonify({"error": "Campos obrigatórios: name, price, quantity"}), 400

    try:
      
        product = ProductService.create_product(
            user_id=user_id,
            name=name,
            price=float(price),
            quantity=int(quantity),
            status=status,
            image_url=image_url 
        )
        return jsonify({
            "message": "Produto criado com sucesso!",
            "product": product.to_dict()
        }), 201
    except Exception as e:
      
        return jsonify({"error": f"Erro ao criar produto: {str(e)}"}), 500




@product_bp.route("/", methods=["GET"])
@jwt_required()
def list_products():
    """
    Lista todos os produtos do usuário autenticado.
    """
    user_id = get_jwt_identity()
    products = ProductService.list_products(user_id)
    return jsonify([p.to_dict() for p in products]), 200


@product_bp.route("/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    """
    Retorna os detalhes de um produto específico.
    """
    user_id = get_jwt_identity()
    product = ProductService.get_product_by_id(product_id, user_id)

    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404

    return jsonify(product.to_dict()), 200


@product_bp.route("/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    """
    Atualiza as informações de um produto.
    """
    user_id = get_jwt_identity()
    data = request.form.to_dict()
    image_file = request.files.get("image")

    product = ProductService.update_product(product_id, user_id, data, image_file)
    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404

    return jsonify({
        "message": "Produto atualizado com sucesso!",
        "product": product.to_dict()
    }), 200


@product_bp.route("/<int:product_id>/status", methods=["PATCH"])
@jwt_required()
def toggle_status(product_id):
    """
    Ativa ou inativa um produto.
    """
    user_id = get_jwt_identity()
    product = ProductService.toggle_status(product_id, user_id)

    if not product:
        return jsonify({"error": "Produto não encontrado"}), 404

    return jsonify({
        "message": f"Status alterado para {product.status}",
        "product": product.to_dict()
    }), 200
