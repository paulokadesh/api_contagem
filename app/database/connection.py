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
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME')
                )
                print("Conectado ao MySQL!")
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            raise

    def get_cursor(self):
        return self.connect().cursor(dictionary=True)

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão com MySQL fechada.") 