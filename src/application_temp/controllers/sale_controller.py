from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.application.service.sale_service import SaleService

class SaleController:
    @staticmethod
    @jwt_required()
    def create_sale():
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Dados JSON são necessários"}), 400)

            product_id = data.get("produtoId")
            quantity = data.get("quantidade")

            if not product_id or not quantity:
                return make_response(jsonify({
                    "erro": "Os campos 'produtoId' e 'quantidade' são obrigatórios"
                }), 400)

            try:
                product_id = int(product_id)
                quantity = int(quantity)
            except ValueError:
                return make_response(jsonify({
                    "erro": "Os campos 'produtoId' e 'quantidade' devem ser números inteiros"
                }), 400)

            seller_id = get_jwt_identity()

            sale, error, status_code = SaleService.register_sale(product_id, quantity, seller_id)
            if error:
                return make_response(jsonify({"erro": error}), status_code)

            return make_response(jsonify({
                "mensagem": "Venda realizada com sucesso",
                "venda": sale.to_dict()
            }), 201)

        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno: {str(e)}"}), 500)

    @staticmethod
    @jwt_required()
    def get_sales():
        try:
            seller_id = get_jwt_identity()
            sales = SaleService.get_sales(seller_id)

            if not sales:
                return make_response(jsonify({
                    "mensagem": "Nenhuma venda encontrada para este vendedor."
                }), 200)

            return make_response(jsonify({"vendas": sales}), 200)

        except Exception as e:
            return make_response(jsonify({"erro": f"Erro interno: {str(e)}"}), 500)
