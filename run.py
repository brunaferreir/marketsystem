import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))


if project_root not in sys.path:
    sys.path.insert(0, project_root)


from flask import Flask
from flask_cors import CORS
from src.config.data_base import init_db, db
from src.routes import init_routes

from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

def create_app():
    """
    Função que cria e configura a aplicação Flask.
    """
    app = Flask(__name__)
    
  
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})

    app.config["JWT_SECRET_KEY"] = "obsidian"
    jwt = JWTManager(app)

    init_db(app)

    init_routes(app)


    with app.app_context():
      
        db.create_all() 

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)