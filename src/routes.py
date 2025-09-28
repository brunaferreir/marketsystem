from src.Application.Controllers.user_controller import UserController
from src.Application.Service.user_service import UserService  
from flask import jsonify, make_response, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def api():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
        
        
#----------------------- ROTA PROTEGIDA (perfil autenticado)
    @app.route('/api/auth/me', methods=['GET'])
    @jwt_required()
    def get_me():
        user_id = get_jwt_identity()
        user = UserService.get_seller_by_id(user_id)

        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404

        return jsonify(user.to_dict()), 200 
    
#----------------------  GET PARA 1 SELLER
    @app.route('/api/sellers/<int:user_id>', methods=['GET'])
    def get_seller_by_id(user_id):
        return UserController.get_seller_by_id(user_id)  
    

#----------------------  POST CRIA UM SELLER
    @app.route('/api/sellers', methods=['POST'])
    def create_seller():
        return UserController.create_seller()    

#----------------------  POST ATIVA SELLER COM CÓDIGO
    @app.route('/api/sellers/activate', methods=['POST'])
    def ativar_seller():
        return UserController.activate_seller()
    
#----------------------  POST LOGIN SELLER
    @app.route('/api/auth/login', methods=['POST'])
    def login_seller():
        return UserController.login_seller()    

#-----------------------  PUT ATUALIZA 1 USUARIO
    @app.route('/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        return UserController.update_user(user_id)

#-----------------------   REDIRECIONA PARA URL DA API
    @app.route('/inicio')
    def inicio():
        return redirect(url_for("api"))    
        
#-----------------------  URL PARA PERFIL COM O ID
    @app.route('/perfil')
    @app.route('/perfil/<int:user_id>')
    def perfil(user_id=None):
        return UserController.get_perfil(user_id) 
    
    #Rota DELETE
    app.route("/Usuários/<int:user_id>", methods=["DELETE"])(UserController.delete_user)
    
    #Rota PATCH para inativar
    app.route("usuário/<int:user_id>/inativar", methods=["PATCH"])(UserController.inactivate_user)