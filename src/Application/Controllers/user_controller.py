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
        status = data.get('status')

        if not name or not cnpj or not email or not password:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, cnpj, email, celular, password, status)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)

    @staticmethod
    def get_all_users():
        """
        Busca e retorna todos os usuários do banco de dados.
        """
        try:
            users = UserService.get_all_users()
            user_list = []
            for user in users:
                user_list.append({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "celular": user.celular,
                    "cnpj": user.cnpj,
                    "status": user.status
                })
            return make_response(jsonify(user_list), 200)
        except Exception as e:
            print(f"Erro ao buscar todos os usuários no serviço: {e}")
            return make_response(jsonify({
                "error": "Ocorreu um erro interno no servidor."
            }), 500)