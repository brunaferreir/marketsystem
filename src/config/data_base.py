import os 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def init_db(app):
    """
    Inicializa a base de dados lendo a DATABASE_URL do ambiente (Render)
    e configura o SQLALCHEMY.
    """
    
    # 1. TENTA OBTER A URL DA VARIÁVEL DE AMBIENTE (RENDER)
    database_url = os.environ.get("DATABASE_URL")
    
    # 2. Configurações da aplicação
    if database_url:
        # Usa a URL externa do ambiente de deploy
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print("INFO: Usando DATABASE_URL do ambiente para conexão remota.")
    else:
        # Fallback local 
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Jujuba345!@localhost:3306/marketsystem'
        print("WARNING: DATABASE_URL não encontrada, usando localhost.")
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # IMPORTANTE: A CHAVE JWT FOI REMOVIDA DAQUI.
    # Ela só está definida em run.py.

    db.init_app(app)
    bcrypt.init_app(app)