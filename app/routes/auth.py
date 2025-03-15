from flask import Blueprint, request, jsonify
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  
    usuario = data.get('usuario')
    senha = data.get('senha')

    print("Dados recebidos:", data)

    if not usuario or not senha:
        return jsonify({'error': 'Usuário e senha são obrigatórios!'}), 400

    user = User()
    result = user.verify_login(usuario, senha)

    print("Resultado do verify_login:", result)

    if not result:
        return jsonify({
            'success': False,
            'mensagem': 'Usuário ou senha inválidos!'
        }), 401

    try:
        response = {
            'success': True,
            'mensagem': 'Login bem-sucedido!',
            'dados': {
                'id': result['ID_USUARIO'],  # Alterado de 'id' para 'ID_USUARIO'
                'nome': result['NOME'],      # Alterado de 'nome' para 'NOME'
                'usuario': result['USUARIO'], # Alterado de 'usuario' para 'USUARIO'
                'permissoes': {
                    'usuarioCabedal': result.get('usuarioCabedal', 0),
                    'usuarioCorte': result.get('usuarioCorte', 0),
                    'usuarioPlanos': result.get('usuarioPlanos', 0),
                    'usuarioStrobel': result.get('UsuarioStrobel', 0),  # Note o U maiúsculo
                    'usuarioIlhos': result.get('UsuarioIlhos', 0),      # Note o U maiúsculo
                    'usuarioExpedicao': result.get('UsuarioExpedicao', 0),
                    'usuarioMapas': result.get('UsuarioMapas', 0),
                    'usuarioInjetora': result.get('UsuarioInjetora', 0),
                    'usuarioPcp': result.get('UsuarioPcp', 0),
                    'usuarioEsteira': result.get('UsuarioEsteira', 0),
                    'usuarioFechamento': result.get('UsuarioFechamento', 0),
                    'usuarioEstoque': result.get('UsuarioEstoque', 0),
                    'usuarioPcpFaturamento': result.get('UsuarioPcpFaturamento', 0),
                    'usuarioVendas': result.get('UsuarioVendas', 0),
                    'usuarioAdm': result.get('UsuarioAdm', 0),
                    'usuarioControladoria': result.get('UsuarioControladoria', 0),
                    'usuarioGerente': result.get('UsuarioGerente', 0)
                }
            }
        }
        return jsonify(response)
    except Exception as e:
        print("Erro ao montar resposta:", str(e))
        print("Conteúdo de result:", result)
        return jsonify({
            'success': False,
            'mensagem': f'Erro interno do servidor: {str(e)}'
        }), 500