from app.database.connection import DatabaseConnection
from datetime import datetime

class Inventory:
    def __init__(self):
        self.db = DatabaseConnection()

    def verify_code(self, codigo_barras):
        cursor = self.db.get_cursor()
        try:
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

    # def get_last_conference(self, codigo_barras):
    #     cursor = self.db.get_cursor()
    #     query = "SELECT emissao FROM contagem_app WHERE codigo = %s AND conferencia = 1 ORDER BY id DESC LIMIT 1"
    #     cursor.execute(query, (codigo_barras,))
    #     result = cursor.fetchone()
    #     cursor.close()       
    #     return result

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
            return last_record
        except Exception as e:
            self.db.connection.rollback()
            raise e
        finally:
            cursor.close()

    # def get_stock_info(self, codigo_barras):
    #     cursor = self.db.get_cursor()
    #     query = "SELECT ITEM, DESCRICAO, QUANT, NUM, REFERENCIA FROM estoque_entradas WHERE CODIGO_BARRAS = %s"
    #     cursor.execute(query, (codigo_barras,))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     return result

    # def get_conference_counts(self, usuario):
    #     cursor = self.db.get_cursor()
    #     query = """
    #         SELECT 
    #             SUM(CASE WHEN conferencia = 1 THEN 1 ELSE 0 END) AS countConferencia1,
    #             SUM(CASE WHEN conferencia = 2 THEN 1 ELSE 0 END) AS countConferencia2
    #         FROM contagem_app
    #         WHERE usuario = %s
    #     """
    #     cursor.execute(query, (usuario,))
    #     result = cursor.fetchone()
    #     cursor.close()       
    #     return result 