from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def init_db(app):
    # Usar banco local MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:Jujuba345!@localhost:3306/marketsystem'
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    print("✅ Banco conectado com sucesso (MySQL local)!")
