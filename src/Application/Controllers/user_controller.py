from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

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


# AQUI--------------------------------- 
    @staticmethod
    def get_user(user_id=None):
        try:
            if user_id:
                user = UserService.get_user(user_id)
                if user:
                    return make_response(jsonify(user.to_dict()), 200)
                else:
                    return make_response(jsonify({
                        "error": "Usuario nao encontrado."
                    }), 404)
            else:
                users = UserService.get_user()
                user_list = [user.to_dict() for user in users]
                return make_response(jsonify(user_list), 200)

        except Exception as e:
            print(f"Erro ao buscar usuário(s) no serviço: {e}")
            return make_response(jsonify({
                "error": "Ocorreu um erro interno no servidor."
            }), 500)


    # AQUI---------------------------------  PUT ATUALIZA 1 USUARIO
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


#Método de controle para buscar um único usuário por ID para a página de perfil.
    @staticmethod
    def get_perfil(user_id=None):
        try:
            if user_id:
                user = UserService.get_user(user_id)
                if user:
                    return f"<h1>Perfil do Usuário: {user.name}</h1><h1>CNPJ: {user.cnpj}</h1><h1>Email: {user.email}</h1> <h1>Celular: {user.celular}</h1> <h1>Senha: {user.password}</h1> <h1>Status: {user.status}</h1>"
                else:
                    return "<h1>Usuário não encontrado</h1>"
            else:
                return "<h1>Página de Perfil Padrão</h1>"
        except Exception as e:
            print(f"Erro ao buscar perfil do usuário: {e}")
            return "Ocorreu um erro ao carregar o perfil.", 500    

 