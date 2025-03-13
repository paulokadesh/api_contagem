from app.database.connection import DatabaseConnection

class User:
    def __init__(self):
        self.db = DatabaseConnection()

    def verify_login(self, usuario, senha):
        cursor = self.db.get_cursor()
        query = "SELECT * FROM usuariosproducao WHERE NOME = %s AND SENHA = %s"
        cursor.execute(query, (usuario, senha))
        result = cursor.fetchone()
        cursor.close()
        return result 