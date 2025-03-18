from app.database.connection import DatabaseConnection
from datetime import datetime

class Inventory:
    def __init__(self):
        self.db = DatabaseConnection()

    def verify_code(self, codigo_barras):
        cursor = self.db.get_cursor()
        try:
            # Limpa o cache antes da consulta
            cursor.execute("FLUSH QUERY CACHE;")
            
            query = "SELECT * FROM estoque_entradas WHERE CODIGO_BARRAS = %s"
            cursor.execute(query, (codigo_barras,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'codigo_barras': result['CODIGO_BARRAS'],
                    'referencia': result['REFERENCIA'],
                    'descricao': result['DESCRICAO'],
                    'numero': result['NUM'],
                    'item': result['ITEM'],
                    'contagem1': result['contagem1']
                }
            return None
        finally:
           cursor.close()

    def register_conference(self, codigo_barras, usuario):
        cursor = self.db.get_cursor()
        try:
            # Insert into contagem_app
            insert_query = "INSERT INTO contagem_app (codigo, conferencia, usuario) VALUES (%s, 1, %s)"
            cursor.execute(insert_query, (codigo_barras, usuario))

            # Update estoque_entradas
            update_query = "UPDATE estoque_entradas SET contagem1 = 1 WHERE CODIGO_BARRAS = %s"
            cursor.execute(update_query, (codigo_barras,))

            # Get last record
            last_query = "SELECT codigo FROM contagem_app WHERE usuario = %s ORDER BY id DESC LIMIT 1"
            cursor.execute(last_query, (usuario,))
            last_record = cursor.fetchone()

            self.db.connection.commit()
            # Limpa o cache após o commit
            cursor.execute("FLUSH QUERY CACHE;")
            return last_record
        except Exception as e:
            self.db.connection.rollback()
            raise e
        finally:
            cursor.close()

    def verificar_produto_caixa(self, numero_caixa, codigo_produto, id_caixa):
        cursor = self.db.get_cursor()
        try:
            # Limpa o cache antes da consulta
            cursor.execute("FLUSH QUERY CACHE;")
            
            # Primeiro, verifica se o produto existe e pega sua data de fabricação
            query_produto = """
                SELECT DATA data_fab, CODIGO_BARRAS, REFERENCIA, DESCRICAO, NUM, ITEM
                FROM estoque_entradas 
                WHERE CODIGO_BARRAS = %s
            """
            cursor.execute(query_produto, (codigo_produto,))
            produto = cursor.fetchone()
            
            if not produto:
                return None, "Produto não encontrado"

            # Verifica se o produto já está em alguma caixa
            query_verificacao = """
                SELECT cdc.*, cmc.COD_CAIXA 
                FROM caixa_dt_conferencia cdc
                JOIN caixas_ms_conferencia cmc ON cmc.ID = cdc.id_caixa
                WHERE cdc.cod_barras = %s
            """
            cursor.execute(query_verificacao, (codigo_produto,))
            caixa_existente = cursor.fetchone()
            
            if caixa_existente:
                return None, f"Produto já está na caixa {caixa_existente['COD_CAIXA']}"

            # Data e hora atual
            data_hora_atual = datetime.now()

            # Registra o produto na caixa usando o id_caixa recebido
            query_insert = """
                INSERT INTO caixa_dt_conferencia 
                (id_caixa, cod_barras, qtde, item, num, data_fab, inclusao) 
                VALUES (%s, %s, 1, %s, %s, %s, %s)
            """
            cursor.execute(query_insert, (
                id_caixa,
                produto['CODIGO_BARRAS'],
                produto['ITEM'],
                produto['NUM'],
                produto['data_fab'],
                data_hora_atual
            ))
            
            # Força o commit imediato
            self.db.connection.commit()
            
            # Limpa o cache da query
            cursor.execute("FLUSH QUERY CACHE;")

            # Fecha o cursor atual antes de abrir um novo
            cursor.close()

            # Após inserir com sucesso, carrega a caixa atualizada
            resultado_caixa = self.carregar_caixa(numero_caixa, "")  # Passamos string vazia como usuário pois não é necessário aqui
            return resultado_caixa, "Produto adicionado à caixa com sucesso"

        except Exception as e:
            self.db.connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

    def carregar_caixa(self, numero_caixa, usuario):
        cursor = self.db.get_cursor()
        try:
            # Limpa o cache antes da consulta
            cursor.execute("FLUSH QUERY CACHE;")
            
            # Busca a caixa e seus produtos usando subquery e LEFT JOIN
            query = """
                SELECT 
                    ms.ID,
                    ms.COD_CAIXA,
                    cdc.qtde,
                    cdc.cod_barras,
                    cdc.item,
                    cdc.num,
                    cdc.data_fab,
                    cdc.inclusao,
                    e.REFERENCIA,
                    e.DESCRICAO
                FROM (
                    SELECT cmc.ID, cmc.COD_CAIXA 
                    FROM caixas_ms_conferencia cmc 
                    WHERE cmc.COD_CAIXA = %s
                ) ms
                LEFT OUTER JOIN caixa_dt_conferencia cdc ON cdc.id_caixa = ms.ID
                LEFT JOIN estoque_entradas e ON cdc.cod_barras = e.CODIGO_BARRAS
            """
            cursor.execute(query, (numero_caixa,))
            resultados = cursor.fetchall()
            
            if not resultados:
                return {
                    'numero_caixa': numero_caixa,
                    'total_produtos': 0,
                    'produtos': [],
                    'usuario_atual': usuario
                }

            # Formata os produtos para retorno
            produtos_formatados = []
            total_produtos = 0
            
            for produto in resultados:
                if produto['cod_barras']:  # Só adiciona se tiver produto (devido ao LEFT JOIN)
                    total_produtos += 1
                    produtos_formatados.append({
                        'codigo_produto': produto['cod_barras'],
                        'referencia': produto['REFERENCIA'],
                        'descricao': produto['DESCRICAO'],
                        'numero': produto['num'],
                        'item': produto['item'],
                        'quantidade': produto['qtde'],
                        'data_fabricacao': produto['data_fab'].isoformat() if produto['data_fab'] else None,
                        'data_inclusao': produto['inclusao'].isoformat() if produto['inclusao'] else None
                    })

            return {
                'numero_caixa': numero_caixa,
                'id_caixa': resultados[0]['ID'] if resultados else None,
                'total_produtos': total_produtos,
                'produtos': produtos_formatados,
                'usuario_atual': usuario
            }

        finally:
            if cursor:
                cursor.close() 