from src.Application.Controllers.user_controller import UserController
from flask import jsonify, make_response, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def api():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
#-AQUI----------------------  POST CRIA UM NOVO USUARIO
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    

#-AQUI----------------------  GET PARA 1 USUARIO
    @app.route('/user/<int:user_id>', methods=['GET'])
    def get_user_by_id(user_id):
        return UserController.get_user(user_id)


#-AQUI----------------------  PUT ATUALIZA 1 USUARIO
    @app.route('/user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        return UserController.update_user(user_id)

#-AQUI----------------------   REDIRECIONA PARA URL DA API
    @app.route('/inicio')
    def inicio():
        return redirect(url_for("api"))    
    
    
#-AQUI----------------------  URL PARA PERFIL COM O ID
    @app.route('/perfil')
    @app.route('/perfil/<int:user_id>')
    def perfil(user_id=None):
        return UserController.get_perfil(user_id)  
      
#-AQUI2----------------------  ROTA DE LOGIN
    @app.route('/login', methods=['POST'])
    def login():
        return UserController.login()

    

        

    
    