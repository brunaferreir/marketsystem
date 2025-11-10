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
    
    # 🔴 NOVO: Rota Raiz (Health Check)
    @app.route('/', methods=['GET'])
    def root_status():
        """Redireciona a raiz para o status da API ou retorna status OK."""
        
        return make_response(jsonify({
            "status": "online",
            "service": "Market System Backend API",
            "message": "Servidor Gunicorn/Flask rodando no Render."
        }), 200)


    @app.route('/api', methods=['GET'])
    def api():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    # rota para pegar o usuário autenticado
    @app.route('/api/auth/me', methods=['GET'])
    @jwt_required()
    def get_me():
        user_id = get_jwt_identity()
        user = UserService.get_seller_by_id(user_id)

        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        return jsonify(user.to_dict()), 200

    # buscar seller por ID
    @app.route('/api/sellers/<int:user_id>', methods=['GET'])
    def get_seller_by_id(user_id):
        return UserController.get_seller_by_id(user_id)

    # criar seller
    @app.route('/api/sellers', methods=['POST'])
    def create_seller():
        return UserController.create_seller()

    # ativar seller (via Twilio)
    @app.route('/api/auth/activate', methods=['POST'])
    def ativar_seller():
        return UserController.activate_seller()

    # login seller
    @app.route('/api/auth/login', methods=['POST'])
    def login_seller():
        return UserController.login_seller()

    # atualizar seller
    @app.route('/api/users/<int:user_id>', methods=['PUT']) # Ajustado para /api
    def update_user(user_id):
        return UserController.update_user(user_id)

    # rota de redirecionamento simples
    @app.route('/inicio')
    def inicio():
        # Redireciona para a nova rota raiz /
        return redirect(url_for("root_status"))

    
    # deletar seller
    @app.route('/api/sellers/<int:user_id>', methods=['DELETE'])
    def delete_seller(user_id):
        return UserController.delete_user(user_id)

   
    app.route("/api/users/<int:user_id>/inactivate", methods=["PATCH"])(UserController.inactivate_user)