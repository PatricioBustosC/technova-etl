import os
import pandas as pd
import pyodbc
import json
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)
load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')

conn_sucia_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DB_SUCIA;Trusted_connection=yes;'

print("Extrayendo transacciones y clientes de DB_SUCIA...")
conn = pyodbc.connect(conn_sucia_str)

df_sql_trans = pd.read_sql("SELECT * FROM transacciones_sucias", conn)
df_sql_trans.columns = ['num_boleta', 'cliente_id', 'sku', 'codigo_canal', 'fecha_transaccion', 'codigo_sucursal', 'cantidad', 'monto_neto']

df_sql_clientes = pd.read_sql("SELECT * FROM cliente_sucio", conn)
df_sql_clientes.columns = ['cliente_id', 'nombre', 'comuna', 'region', 'segmento']
conn.close()

print("Extrayendo transacciones de Excel...")
excel_path = os.path.join('fuentes_info_sucia', 'excel_fuente_tnr.xlsx')
df_excel_trans = pd.read_excel(excel_path)
df_excel_trans.columns = ['num_boleta', 'cliente_id', 'sku', 'codigo_canal', 'fecha_transaccion', 'codigo_sucursal', 'cantidad', 'monto_neto']

print("Extrayendo transacciones de JSON...")
json_path = os.path.join('fuentes_info_sucia', 'json_fuente_tnr.json')
with open(json_path, 'r', encoding='utf-8') as f:
    df_json_trans = pd.DataFrame(json.load(f))
df_json_trans.columns = ['num_boleta', 'cliente_id', 'sku', 'codigo_canal', 'fecha_transaccion', 'codigo_sucursal', 'cantidad', 'monto_neto']

print("Extrayendo clientes de JSON...")
json_clientes_path = os.path.join('fuentes_info_sucia', 'clientes_fuente_tnr.json')
with open(json_clientes_path, 'r', encoding='utf-8') as f:
    df_json_clientes = pd.DataFrame(json.load(f))
df_json_clientes.columns = ['cliente_id', 'nombre', 'comuna', 'region', 'segmento']

df_crudo_trans = pd.concat([df_sql_trans, df_excel_trans, df_json_trans], ignore_index=True)
df_crudo_trans.to_csv('datos_crudos.csv', index=False)

df_crudo_clientes = pd.concat([df_sql_clientes, df_json_clientes], ignore_index=True)
df_crudo_clientes.to_csv('clientes_crudos.csv', index=False)

print(f"Extraccion terminada. Transacciones: {len(df_crudo_trans)} | Clientes: {len(df_crudo_clientes)}")