import os 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def init_db(app):
    """
    Inicializa a base de dados e configura a chave JWT, priorizando variáveis de ambiente.
    """
    
    # 1. TENTA OBTER A URL DA VARIÁVEL DE AMBIENTE (RENDER/RAILWAY)
    database_url = os.environ.get("DATABASE_URL")
    
    # 2. Configurações da aplicação
    if database_url:
        # Usa a URL externa (Railway)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print("INFO: Usando DATABASE_URL do ambiente para conexão remota.")
    else:
        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Jujuba345!@localhost:3306/marketsystem'
        print("WARNING: DATABASE_URL não encontrada, usando localhost.")
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
   
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "obsidian") 

    db.init_app(app)
    bcrypt.init_app(app)