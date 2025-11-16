from flask import request, jsonify, make_response
from src.application.service.user_service import UserService
from flask_jwt_extended import create_access_token, jwt_required, create_access_token, get_jwt_identity


class UserController:
    @staticmethod
    def register_user():
        try:    
            data = request.get_json()

            if not data:
                return make_response(jsonify({"erro": "Dados JSON necessários"}), 400)

            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            cnpj = data.get('cnpj')
            number = data.get('number')

            if not name or not email or not password or not cnpj or not number:
                return make_response(jsonify({"erro": "Missing required fields"}), 400)
            
            user = UserService.create_user(name, email, password, cnpj, number)
            return make_response(jsonify({
                "mensagem": "User salvo com sucesso",
                "usuario": user.to_dict()
            }), 201)
        
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)


    @staticmethod
    @jwt_required()
    def get_user(idUser):
        try:
            user = UserService.get_user(idUser)
            if not user:
                return {"erro": "Usuário não encontrado"}, 404
            return make_response(jsonify({
                "usuario": user.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)



    @staticmethod
    @jwt_required()
    def update_user(idUser):
        try:
            current_user_id = get_jwt_identity()

            if str(current_user_id) != str(idUser):
                return make_response(jsonify({"erro": "Não autorizado"}), 403)

            new_data = request.get_json()
            if not new_data:
                return make_response(jsonify({"erro": "Nenhum dado enviado para atualização"}), 400)

        
            allowed_fields = ["name", "email", "password", "cnpj", "number", "status"]
            update_fields = {key: value for key, value in new_data.items() if key in allowed_fields}

            if not update_fields:
                return make_response(jsonify({"erro": "Nenhum campo válido enviado"}), 400)

            user = UserService.update_user(idUser, update_fields)
            if not user:
                return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)

            return make_response(jsonify({
                "mensagem": "User atualizado com sucesso",
                "usuario": user.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    @jwt_required()
    def inativar_user(idUser):
        try:
            current_user_id = get_jwt_identity()

            # Garante que um usuário só pode inativar a si mesmo
            if str(current_user_id) != str(idUser):
                return make_response(jsonify({"erro": "Não autorizado"}), 403)

            user = UserService.inativar_user(idUser)
            if not user:
                return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)
            return make_response(jsonify({"mensagem": "Usuário inativado!"}), 200)
        
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

  

    @staticmethod
    def ativar_user():
        try:
            data = request.get_json()
            number = data.get("number")
            code = data.get("code")

            user, erro = UserService.ativar_user(number,code)
            if erro:
                return make_response(jsonify({"erro": erro}), 400)

            return make_response(jsonify({
                "mensagem" : "Usuário ativado com sucesso",
                "usuario" : user.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({"erro" : str(e)}), 500)
        

    @staticmethod
    def login():
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            user, erro = UserService.autenticacao(email, password)
            if erro:
                return make_response(jsonify({"erro": erro}), 401)

            access_token = create_access_token(identity=str(user.id))

            return jsonify({
                "access_token": access_token,
                "usuario": user.to_dict()
            }), 200

        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

