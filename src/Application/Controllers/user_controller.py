from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService
from flask_jwt_extended import create_access_token

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        celular = data.get('celular')
        password = data.get('password')
        status = data.get('status', 'inativo')

        if not all([name, cnpj, email, celular, password]):
            return make_response(jsonify({"erro": "Dados inválidos todos os campos são obrigatórios"}), 400)

        user = UserService.create_user(name, cnpj, email, celular, password, status)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)

#---------------------------------BUSCAR SELLER POR ID 
    @staticmethod
    def get_seller_by_id(user_id=None):
        try:
            if user_id:
                seller = UserService.get_seller_by_id(user_id)
                if seller:
                    return make_response(jsonify(seller.to_dict()), 200)
                else:
                    return make_response(jsonify({
                        "error": "Usuario nao encontrado."
                    }), 404)
            else:
                users = UserService.get_seller_by_id()
                user_list = [seller.to_dict() for seller in users]
                return make_response(jsonify(user_list), 200)

        except Exception as e:
            print(f"Erro ao buscar usuário(s) no serviço: {e}")
            return make_response(jsonify({
                "error": "Ocorreu um erro interno no servidor."
            }), 500)
        
#---------------------- POST CADASTRAR SELLER
    @staticmethod
    def create_seller():
        data = request.json
        if not data:
            return make_response(jsonify({"erro": "Dados inválidos"}), 400)
        
        result = UserService.create_seller(
            data.get("nome"),
            data.get("cnpj"),
            data.get("email"),
            data.get("celular"),
            data.get("senha")
        )
        return jsonify(result), 200
    
#---------------------- POST ATIVA SELLER COM CÓDIGO
    @staticmethod
    def activate_seller():
        data = request.json
        if not data:
            return make_response(jsonify({"erro": "Dados inválidos"}), 400)
            
        result = UserService.activate_seller(
            data.get("celular"),
            data.get("codigo")
        )
        return jsonify(result), 200    

#--------------------------------- POST LOGIN SELLER
    @staticmethod
    def login_seller():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return make_response(jsonify({"erro": "Email e senha são obrigatórios"}), 400)

            seller = UserService.authenticate_user(email, password)

            if seller:
                access_token = create_access_token(identity=seller.id)
                return jsonify({"token": access_token}), 200
            else:
                return make_response(jsonify({"erro": "Credenciais inválidas"}), 401)
        
        except Exception as e:
            print(f"Erro no login: {e}")
            return make_response(jsonify({"erro": "Ocorreu um erro interno ao tentar fazer login."}), 500)  

#---------------------------------  PUT ATUALIZA 1 SELLER
    @staticmethod
    def update_user(user_id):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"erro": "Nenhum dado fornecido para atualização"}), 400)
            
            user = UserService.update_user(user_id, data)
            
            if user:
                return make_response(jsonify({
                    "mensagem": "Usuário atualizado com sucesso",
                    "usuario": user.to_dict()
                }), 200)
            else:
                return make_response(jsonify({
                    "erro": "Usuário não encontrado."
                }), 404)

        except Exception as e:
            print(f"Erro ao atualizar usuário no serviço: {e}")
            return make_response(jsonify({
                "erro": "Ocorreu um erro interno ao tentar atualizar o usuário."
            }), 500)

#--------------------------------------ID para a página de perfil dp seller.
    @staticmethod
    def get_perfil(user_id=None):
        try:
            if user_id:
                seller = UserService.get_seller_by_id(user_id)
                if seller:
                    return f"<h1>Perfil do Usuário: {seller.name}</h1><h1>CNPJ: {seller.cnpj}</h1><h1>Email: {seller.email}</h1> <h1>Celular: {seller.celular}</h1> <id>Senha: {seller.password}</h1> <h1>Status: {seller.status}</h1>"
                else:
                    return "<h1>Usuário não encontrado</h1>"
            else:
                return "<h1>Página de Perfil Padrão</h1>"
        except Exception as e:
            print(f"Erro ao buscar perfil do usuário: {e}")
            return "Ocorreu um erro ao carregar o perfil.", 500    
        
    @staticmethod
    def delete_user(user_id):
        try:
            sucess = UserService.delete_user(user_id)
            if sucess:
                return make_response(jsonify({"mensagem": "Usuário deleteado com sucesso"}), 200)
            else:
                return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            return make_response(jsonify({"erro": "Erro interno ao tentar deletar  o usuário"}), 500)
        
        
    @staticmethod
    def inactivate_user(user_id):
        try:
            user = UserService.inactivate_user(user_id)
            if user:
                return make_response(jsonify({
                    "mensagem": "Uuário inativado com sucesso",
                    "usuario": user.to_dict()
                }), 200)
            else:
                return make_response(jsonify({"Erro": "Usuário não encontrado"}), 404)
        except Exception as e:
            print(f"Erro ao inativar usuário: {e}")
            return make_response(jsonify({"Erro": "Erro interno  ao tentar inativar o usuário"}), 500)
            