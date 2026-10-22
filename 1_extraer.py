import os
import pandas as pd
import pyodbc
import json
from dotenv import load_dotenv

# Carga las variables seguras
load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')

conn_sucia_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DB_SUCIA;Trusted_connection=yes;'

print("📥 1. Extrayendo datos de DB_SUCIA...")
conn = pyodbc.connect(conn_sucia_str)
df_sql = pd.read_sql("SELECT * FROM transacciones_sucias", conn)
conn.close()
df_sql.columns = ['id_transaccion', 'rut', 'sku', 'canal', 'fecha', 'tienda', 'cantidad', 'monto']

print("📥 2. Extrayendo datos de Excel...")
excel_path = os.path.join('fuentes_info_sucia', 'excel_fuente_tnr.xlsx')
df_excel = pd.read_excel(excel_path)
df_excel.columns = ['id_transaccion', 'rut', 'sku', 'canal', 'fecha', 'tienda', 'cantidad', 'monto']

print("📥 3. Extrayendo datos de JSON...")
json_path = os.path.join('fuentes_info_sucia', 'json_fuente_tnr.json')
with open(json_path, 'r', encoding='utf-8') as f:
    df_json = pd.DataFrame(json.load(f))
df_json.columns = ['id_transaccion', 'rut', 'sku', 'canal', 'fecha', 'tienda', 'cantidad', 'monto']

# Unificar todo en un solo archivo
df_crudo = pd.concat([df_sql, df_excel, df_json], ignore_index=True)
df_crudo.to_csv('datos_crudos.csv', index=False)
print(f"✅ Extracción completada. {len(df_crudo)} registros guardados en 'datos_crudos.csv'.")