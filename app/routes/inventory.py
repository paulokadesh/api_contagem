from flask import Blueprint, request, jsonify
from app.models.inventory import Inventory
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/verificar_codigo', methods=['POST'])
def verify_code():
    data = request.get_json()  
    codigo_barras = data.get('codigoBarras')
    usuario = data.get('usuario')
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"dados recebidos: {data}")

    if not codigo_barras or not usuario:
        return jsonify({
            'success': False,
            'mensagem': 'Código de barras e usuário são obrigatórios!',
            'dados': None
        }), 400

    try:
        inventory = Inventory()
        
        # Verify if code exists
        code_result = inventory.verify_code(codigo_barras)
    
        if not code_result:  # Corrigido de 'result' para 'code_result'
            return jsonify({
                'success': False,
                'mensagem': 'Produto não encontrado',
                'dados': None
            }), 404
           # Se já está conferido (contagem1 = 1), retorna erro
        if code_result['contagem1'] == 1:
            return jsonify({
                'success': False,
                'mensagem': 'Produto já conferido',
                'dados': None
            })

        # Verifica última conferência
        # last_conference = inventory.get_last_conference(codigo_barras)
        # if last_conference:
        #     emissao = last_conference['emissao']
        #     emissao_formatada = emissao.strftime("%d/%m/%Y %H:%M:%S")
        #     return jsonify({
        #         'success': False,
        #         'mensagem': f'Material já conferido em {emissao_formatada} por {last_conference["nome_usuario"]}',
        #         'dados': None
        #     })

        # Registra a conferência
        conference_result = inventory.register_conference(codigo_barras, usuario)
        
        return jsonify({
            'success': True,
            'mensagem': 'Produto verificado com sucesso!',
            'dados': {
                'codigo_barras': code_result['codigo_barras'],
                'referencia': code_result['referencia'],
                'descricao': code_result['descricao'],
                'data_conferencia': datetime.now().isoformat(),
                'usuario': usuario,
                'numero': code_result['numero'],
                'item': code_result['item']
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'mensagem': f'Erro ao verificar produto: {str(e)}',
            'dados': None
        }), 500


# @inventory_bp.route('/buscar_estoque', methods=['POST'])
# def get_stock():
#     data = request.get_json()
#     codigo_barras = data.get('codigoBarras')

#     if not codigo_barras:
#         return jsonify({'error': 'Código de barras é obrigatório!'}), 400

#     inventory = Inventory()
#     result = inventory.get_stock_info(codigo_barras)

#     if not result:
#         return jsonify({'mensagem': 'Código não encontrado no estoque!'})

#     return jsonify(result)


# @inventory_bp.route('/conferencias', methods=['POST'])
# def get_conferences():
#     data = request.get_json()
#     usuario = data.get('usuario')

#     if not usuario:
#         return jsonify({'error': 'Usuário é obrigatório!'}), 400

#     inventory = Inventory()
#     result = inventory.get_conference_counts(usuario)

#     count_conferencia1 = result['countConferencia1'] or 0
#     count_conferencia2 = result['countConferencia2'] or 0
#     diferenca = count_conferencia1 - count_conferencia2

#     return jsonify({
#         'countConferencia1': count_conferencia1,
#         'countConferencia2': count_conferencia2,
#         'diferenca': diferenca
#     })

@inventory_bp.route('/verificar_produto_caixa', methods=['POST'])
def verificar_produto_caixa():
    data = request.get_json()
    
    # Validação dos dados recebidos
    numero_caixa = data.get('numeroCaixa')
    codigo_produto = data.get('codigoProduto')
    id_caixa = data.get('id_caixa')

    if not all([numero_caixa, codigo_produto, id_caixa]):
        return jsonify({
            'success': False,
            'mensagem': 'Todos os campos são obrigatórios: numeroCaixa, codigoProduto e id_caixa',
            'dados': None
        }), 400

    try:
        inventory = Inventory()
        resultado, mensagem = inventory.verificar_produto_caixa(numero_caixa, codigo_produto, id_caixa)

        if not resultado:
            return jsonify({
                'success': False,
                'mensagem': mensagem,
                'dados': None
            }), 404

        return jsonify({
            'success': True,
            'mensagem': mensagem,
            'dados': resultado
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'mensagem': f'Erro ao verificar produto na caixa: {str(e)}',
            'dados': None
        }), 500

@inventory_bp.route('/carregar_caixa', methods=['POST'])
def carregar_caixa():
    data = request.get_json()
    print(f"dados recebidos: {data}")
    
    # Validação dos dados recebidos
    numero_caixa = data.get('numeroCaixa')
    usuario = data.get('usuario')

    if not all([numero_caixa, usuario]):
        return jsonify({
            'success': False,
            'mensagem': 'Número da caixa e usuário são obrigatórios',
            'dados': None
        }), 400

    try:
        inventory = Inventory()
        resultado = inventory.carregar_caixa(numero_caixa, usuario)

        return jsonify({
            'success': True,
            'mensagem': 'Caixa carregada com sucesso',
            'dados': resultado
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'mensagem': f'Erro ao carregar caixa: {str(e)}',
            'dados': None
        }), 500
    print(response.json()['dados']['total_produtos'])