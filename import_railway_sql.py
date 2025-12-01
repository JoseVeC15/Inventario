#!/usr/bin/env python3
"""
Script para importar el schema SQL a Railway MySQL
"""
import MySQLdb
import os

# Credenciales de Railway (obtenidas de railway variables)
DB_CONFIG = {
    'host': 'metro.proxy.rlwy.net',
    'port': 58171,
    'user': 'root',
    'password': 'zhcejBCoCBfBDUgOuzMUwAbVRfKFgiOB',
    'database': 'railway',
    'charset': 'utf8mb4'
}

def import_sql():
    """Importa el archivo SQL a Railway"""
    print("Conectando a Railway MySQL...")
    
    try:
        # Conectar a la base de datos
        conn = MySQLdb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✓ Conexión exitosa!")
        print("Importando schema SQL...")
        
        # Leer el archivo SQL adaptado
        with open('.docker/mysql/database/init_railway.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir por comandos individuales
        commands = sql_content.split(';')
        
        # Ejecutar cada comando
        for i, command in enumerate(commands, 1):
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    print(f"✓ Comando {i}/{len(commands)} ejecutado")
                except Exception as e:
                    if 'already exists' not in str(e):
                        print(f"⚠ Warning en comando {i}: {e}")
        
        conn.commit()
        print("\n✓ Schema importado correctamente!")
        print("\nUsuarios de prueba creados:")
        print("- Admin: admin / admin123")
        print("- Vendedor: jperez / vendedor123")
        print("- Almacenero: mgonzalez / almacen123")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    import_sql()
