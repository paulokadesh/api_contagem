from flask import Blueprint, request, jsonify
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  
    usuario = data.get('usuario')
    senha = data.get('senha')

    if not usuario or not senha:
        return jsonify({'error': 'Usuário e senha são obrigatórios!'}), 400

    user = User()
    result = user.verify_login(usuario, senha)

    if not result:
        return jsonify({'error': 'Usuário ou senha inválidos!'}), 401

    return jsonify({'mensagem': 'Login bem-sucedido!'}) 