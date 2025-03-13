from app.database.connection import DatabaseConnection

def check_changes():
    db = DatabaseConnection()
    cursor = db.get_cursor()
    
    # Verificar últimas inserções na contagem_app
    cursor.execute("""
        SELECT * FROM contagem_app 
        ORDER BY id DESC 
        LIMIT 5
    """)
    print("\nÚltimas inserções na contagem_app:")
    for row in cursor.fetchall():
        print(row)
    
    # Verificar registros atualizados no estoque_entradas
    cursor.execute("""
        SELECT CODIGO_BARRAS, contagem1 
        FROM estoque_entradas 
        WHERE contagem1 = 1
        LIMIT 5
    """)
    print("\nRegistros atualizados em estoque_entradas:")
    for row in cursor.fetchall():
        print(row)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    check_changes() 