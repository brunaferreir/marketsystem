from src.Application.Controllers.user_controller import UserController
from src.Application.Service.user_service import UserService
from src.Application.Controllers.product_controller import product_bp  # ✅ blueprint de produtos
from src.Application.Controllers.sale_controller import sale_bp  # ✅ blueprint de vendas

from flask import jsonify, make_response, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity


def init_routes(app):
    """
    Inicializa e registra todas as rotas principais da aplicação.
    """

    # ✅ registra blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(sale_bp)

    # 🔹 rota de verificação básica
    @app.route('/api', methods=['GET'])
    def api():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    # 🔹 rota para pegar o usuário autenticado
    @app.route('/api/auth/me', methods=['GET'])
    @jwt_required()
    def get_me():
        user_id = get_jwt_identity()
        user = UserService.get_seller_by_id(user_id)

        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        return jsonify(user.to_dict()), 200

    # 🔹 buscar seller por ID
    @app.route('/api/sellers/<int:user_id>', methods=['GET'])
    def get_seller_by_id(user_id):
        return UserController.get_seller_by_id(user_id)

    # 🔹 criar seller
    @app.route('/api/sellers', methods=['POST'])
    def create_seller():
        return UserController.create_seller()

    # 🔹 ativar seller (via Twilio)
    @app.route('/api/sellers/activate', methods=['POST'])
    def ativar_seller():
        return UserController.activate_seller()

    # 🔹 login seller
    @app.route('/api/auth/login', methods=['POST'])
    def login_seller():
        return UserController.login_seller()

    # 🔹 atualizar seller
    @app.route('/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        return UserController.update_user(user_id)

    # 🔹 rota de redirecionamento simples
    @app.route('/inicio')
    def inicio():
        return redirect(url_for("api"))

    # 🔹 visualizar perfil
    @app.route('/perfil')
    @app.route('/perfil/<int:user_id>')
    def perfil(user_id=None):
        return UserController.get_perfil(user_id)

    # 🔹 deletar seller
    @app.route('/api/sellers/<int:user_id>', methods=['DELETE'])
    def delete_seller(user_id):
        return UserController.delete_user(user_id)

    # 🔹 inativar seller
    app.route("/usuario/<int:user_id>/inativar", methods=["PATCH"])(UserController.inactivate_user)
