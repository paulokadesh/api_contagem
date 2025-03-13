from flask import Flask
from flask_cors import CORS
from app.routes.auth import auth_bp
from app.routes.inventory import inventory_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(inventory_bp)

if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 8082))
    app.run(host='0.0.0.0', port=port) 