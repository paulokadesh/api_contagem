import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        try:
            # Sempre fecha a conexão existente antes de criar uma nova
            if self.connection:
                self.close()

            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                autocommit=False,  # Desabilita autocommit para controle manual
                pool_reset_session=True,  # Reseta a sessão ao retornar à pool
                pool_size=5,  # Tamanho da pool de conexões
                pool_name="mypool"
            )
            print("Conectado ao MySQL!")
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise

    def get_cursor(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            return self.connection.cursor(dictionary=True, buffered=True)
        except Error as e:
            print(f"Erro ao obter cursor: {e}")
            raise

    def close(self):
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                self.connection = None
                print("Conexão com MySQL fechada.")
        except Error as e:
            print(f"Erro ao fechar conexão: {e}")
            raise 