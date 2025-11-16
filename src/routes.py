from src.application.controllers.user_controller import UserController
from src.application.controllers.product_controller import ProductController
from src.application.controllers.sale_controller import SaleController
from flask import jsonify, make_response

def init_routes(app):
    
    # User routes
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up"
        }), 200)

    @app.route('/user/<int:id>', methods= ['GET'] )
    def get_user(id):
        return UserController.get_user(id)
    
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()
    
    @app.route('/user/<int:id>', methods=['PUT'])
    def update_user(id):  
        return UserController.update_user(id)
    
    @app.route('/user/<int:id>/inativar', methods= ['PUT'] )
    def inativar_user(id):
        return UserController.inativar_user(id)

    @app.route('/user/ativar', methods=['POST'])
    def ativar_user():
        return UserController.ativar_user()
    
    @app.route('/login', methods= ['POST'])
    def login():
        return UserController.login()
    
    
    # Products routes
    @app.route('/product', methods=['POST'])
    def register_product():
        return ProductController.register_product()
    
    @app.route('/product', methods=['GET'])
    def get_products():
        return ProductController.get_products()
    
    @app.route('/product/<int:id>', methods=['GET'])
    def get_product_id(id):
        return ProductController.get_product_id(id)
    
    @app.route('/product/<int:id>', methods=['PUT'])
    def update_product(id):
        return ProductController.update_product(id)
    
    @app.route('/product/<int:id>/inativar', methods=['PUT'])
    def inativar_product(id):
        return ProductController.inativar_product(id)

    # Sales routes
    @app.route('/sale', methods=['POST'])
    def create_sale():
        return SaleController.create_sale()
    
    @app.route('/sale', methods=['GET'])
    def get_sales():
        return SaleController.get_sales()
