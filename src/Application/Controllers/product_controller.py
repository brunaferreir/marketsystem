from flask import request, jsonify, make_response, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from src.application.service.product_service import ProductService
import os


# Pasta onde as imagens serão salvas
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class ProductController:
    @staticmethod
    @jwt_required()
    def register_product():
        try:
            # ✅ Aceita multipart/form-data (com imagem)
            name = request.form.get("name")
            price = request.form.get("price")
            quantity = request.form.get("quantity")
            status = request.form.get("status", "active")
            image = request.files.get("image")

            # ID do vendedor via token JWT
            seller_id = get_jwt_identity()

            # ⚠️ Verifica campos obrigatórios
            if not name or not price or not quantity:
                return make_response(jsonify({"erro": "Campos obrigatórios: name, price, quantity"}), 400)

            # 📸 Salvar imagem se houver
            image_url = None
            if image:
                filename = secure_filename(image.filename)
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                image.save(save_path)
                image_url = f"/uploads/{filename}"

            # ✅ Criação do produto via serviço
            product = ProductService.create_product(
                name=name,
                price=float(price),
                quantity=int(quantity),
                status=status,
                image_url=image_url,
                seller_id=seller_id
            )

            return make_response(jsonify({
                "mensagem": "Produto criado com sucesso",
                "produto": product.to_dict()
            }), 201)

        except Exception as e:
            print("Erro ao cadastrar produto:", e)
            return make_response(jsonify({"erro": str(e)}), 500)

    # ----------------------------------------------------------------------

    @staticmethod
    @jwt_required()
    def get_products():
        try:
            seller_id = get_jwt_identity()
            products = ProductService.get_products(seller_id)

            if not products:
                return make_response(jsonify({"erro": "Não há produtos cadastrados"}), 404)

            return make_response(jsonify({
                "produtos": [product.to_dict() for product in products]
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    # ----------------------------------------------------------------------

    @staticmethod
    @jwt_required()
    def get_product_id(id):
        try:
            current_seller_id = get_jwt_identity()
            product = ProductService.get_product_id(id)

            if not product:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            if str(product.seller_id) != str(current_seller_id):
                return make_response(jsonify({"erro": "Acesso não autorizado a este produto"}), 403)

            return make_response(jsonify({"produto": product.to_dict()}), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    # ----------------------------------------------------------------------

    @staticmethod
    @jwt_required()
    def update_product(id):
        try:
            current_seller_id = get_jwt_identity()
            product = ProductService.get_product_id(id)

            if not product:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            if str(product.seller_id) != str(current_seller_id):
                return make_response(jsonify({"erro": "Não autorizado. Você não é o vendedor deste produto."}), 403)

            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Dados JSON necessários para atualização"}), 400)

            updated_product = ProductService.update_product(id, data)

            return make_response(jsonify({
                "mensagem": "Produto atualizado com sucesso",
                "produto": updated_product.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    # ----------------------------------------------------------------------

    @staticmethod
    @jwt_required()
    def inativar_product(id):
        try:
            current_seller_id = get_jwt_identity()
            product = ProductService.get_product_id(id)

            if not product:
                return make_response(jsonify({"erro": "Produto não encontrado"}), 404)

            if str(product.seller_id) != str(current_seller_id):
                return make_response(jsonify({"erro": "Não autorizado. Você não é o vendedor deste produto."}), 403)

            inactivated_product = ProductService.inativar_product(id)

            return make_response(jsonify({
                "mensagem": "Produto inativado com sucesso",
                "produto": inactivated_product.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)


# ----------------------------------------------------------------------
# 🔗 Rota auxiliar para servir imagens (adicione isso em app.py também)
def serve_uploaded_image(filename):
    """Serve arquivos da pasta /uploads"""
    return send_from_directory(UPLOAD_FOLDER, filename)
