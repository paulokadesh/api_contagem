from flask import Flask, send_from_directory
from flask_cors import CORS
from app.routes.auth import auth_bp
from app.routes.inventory import inventory_bp
from app.swagger import swagger_ui_blueprint, SWAGGER_URL
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='app/static')
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('app/static', path)

if __name__ == '__main__':
    port = int(os.getenv('APP_PORT', 8082))
    app.run(host='0.0.0.0', port=port, debug=True) 