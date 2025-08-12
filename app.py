from flask import Flask
from controllers.item_controller import item_bp

app = Flask(__name__)
app.register_blueprint(item_bp)

if __name__ == "__main__":
    app.run(debug=True)


