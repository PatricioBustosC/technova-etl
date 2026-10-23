import os
import pyodbc

SERVER = '127.0.0.1'
DRIVER = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={DRIVER};SERVER={SERVER};Trusted_connection=yes;'
print("Conectando a SQL Server...")
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

db_name = 'DB_SUCIA'

print(f"Eliminando {db_name} si existe...")
cursor.execute(f"""
    IF EXISTS (SELECT * FROM sys.databases WHERE name = '{db_name}')
    BEGIN
        ALTER DATABASE [{db_name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
        DROP DATABASE [{db_name}];
    END
""")

print(f"Creando {db_name}...")
cursor.execute(f"CREATE DATABASE [{db_name}];")
cursor.close()
conn.close()

conn_db_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={db_name};Trusted_connection=yes;'
conn_db = pyodbc.connect(conn_db_str, autocommit=True)
cursor_db = conn_db.cursor()

sql_file_path = os.path.join('fuentes_info_sucia', 'db_sucia_inserts.sql')

if os.path.exists(sql_file_path):
    print("Ejecutando script SQL...")
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        
    commands = sql_script.split(';')
    for cmd in commands:
        cmd_clean = cmd.strip()
        if cmd_clean and not cmd_clean.upper().startswith("CREATE DATABASE") and not cmd_clean.upper().startswith("USE "):
            try:
                cursor_db.execute(cmd_clean)
            except Exception as e:
                print(f"Aviso: {e}")
                
    print("Base de datos creada y poblada.")
else:
    print("Error: Archivo no encontrado.")

cursor_db.close()
conn_db.close()