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

    if not codigo_barras or not usuario:
        return jsonify({'error': 'Código de barras e usuário são obrigatórios!'}), 400

    inventory = Inventory()
    
    # Verify if code exists
    code_result = inventory.verify_code(codigo_barras)
    if not code_result:
        return jsonify({'mensagem': 'CÓDIGO NÃO ENCONTRADO!'})

    # Check last conference
    last_conference = inventory.get_last_conference(codigo_barras)
    if last_conference:
        emissao = last_conference['emissao']
        emissao_formatada = emissao.strftime("%d/%m/%Y %H:%M:%S")
        return jsonify({'mensagem': f'MATERIAL JÁ CONFERIDO! {emissao_formatada}'})

    # Register conference
    last_record = inventory.register_conference(codigo_barras, usuario)
    ultimo_codigo = last_record['codigo'] if last_record else "NENHUM CÓDIGO ENCONTRADO!"

    return jsonify({
        'mensagem': f'CONFERÊNCIA REALIZADA COM SUCESSO! {data_hora_atual} (AGORA)',
        'ultimoCodigo': ultimo_codigo
    })

@inventory_bp.route('/buscar_estoque', methods=['POST'])
def get_stock():
    data = request.get_json()
    codigo_barras = data.get('codigoBarras')

    if not codigo_barras:
        return jsonify({'error': 'Código de barras é obrigatório!'}), 400

    inventory = Inventory()
    result = inventory.get_stock_info(codigo_barras)

    if not result:
        return jsonify({'mensagem': 'Código não encontrado no estoque!'})

    return jsonify(result)

@inventory_bp.route('/conferencias', methods=['POST'])
def get_conferences():
    data = request.get_json()
    usuario = data.get('usuario')

    if not usuario:
        return jsonify({'error': 'Usuário é obrigatório!'}), 400

    inventory = Inventory()
    result = inventory.get_conference_counts(usuario)

    count_conferencia1 = result['countConferencia1'] or 0
    count_conferencia2 = result['countConferencia2'] or 0
    diferenca = count_conferencia1 - count_conferencia2

    return jsonify({
        'countConferencia1': count_conferencia1,
        'countConferencia2': count_conferencia2,
        'diferenca': diferenca
    }) 