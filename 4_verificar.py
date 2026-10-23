import pyodbc
import pandas as pd
import os
import json
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')

print("\nREPORTE DE AUDITORIA (ETL)\n")

print("1. FUENTES ORIGEN")
try:
    conn_sucia = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DB_SUCIA;Trusted_connection=yes;')
    df_sucia_trans = pd.read_sql("SELECT COUNT(*) as total FROM transacciones_sucias", conn_sucia)
    df_sucia_cli = pd.read_sql("SELECT COUNT(*) as total FROM cliente_sucio", conn_sucia)
    print(f"- DB_SUCIA (SQL): {df_sucia_trans.iloc[0]['total']} transacciones | {df_sucia_cli.iloc[0]['total']} clientes")
    conn_sucia.close()
except Exception as e:
    print(f"- Error DB_SUCIA: {e}")

try:
    ruta_excel = os.path.join('fuentes_info_sucia', 'excel_fuente_tnr.xlsx')
    if os.path.exists(ruta_excel):
        df_excel = pd.read_excel(ruta_excel)
        print(f"- Excel: {len(df_excel)} transacciones")
    else:
        print("- Excel: Archivo no encontrado")
except Exception as e:
    print(f"- Error Excel: {e}")

try:
    ruta_json_t = os.path.join('fuentes_info_sucia', 'json_fuente_tnr.json')
    if os.path.exists(ruta_json_t):
        with open(ruta_json_t, 'r', encoding='utf-8') as f:
            print(f"- JSON (Transacciones): {len(json.load(f))} transacciones")
    else:
        print("- JSON (Transacciones): Archivo no encontrado")
except Exception as e:
    print(f"- Error JSON Transacciones: {e}")

try:
    ruta_json_c = os.path.join('fuentes_info_sucia', 'clientes_fuente_tnr.json')
    if os.path.exists(ruta_json_c):
        with open(ruta_json_c, 'r', encoding='utf-8') as f:
            print(f"- JSON (Clientes): {len(json.load(f))} clientes")
    else:
        print("- JSON (Clientes): Archivo no encontrado")
except Exception as e:
    print(f"- Error JSON Clientes: {e}")

print("\n2. AUDITORIA ETL (DataRetail360_DW)")
try:
    conn_dw = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DataRetail360_DW;Trusted_connection=yes;')
    
    print("--- HISTORIAL DE EJECUCION ---")
    df_logs = pd.read_sql("SELECT log_id, nombre_paquete, estado, filas_cargadas, filas_rechazadas FROM etl_log_ejecucion ORDER BY log_id DESC", conn_dw)
    if df_logs.empty:
        print("Sin registros en el log.\n")
    else:
        print(df_logs.head(5).to_string(index=False))
        print("\n")

    print("--- RECHAZOS ---")
    df_rechazos = pd.read_sql("SELECT rechazo_id, origen, motivo_rechazo FROM tabla_rechazos", conn_dw)
    if df_rechazos.empty:
        print("Sin registros de rechazo.\n")
    else:
        print(df_rechazos.to_string(index=False))
        print("\n")
        
    conn_dw.close()
except Exception as e:
    print(f"Error DataRetail360_DW: {e}")

print("3. DATOS LIMPIOS")
ruta_trans = 'datos_limpios.csv'
if os.path.exists(ruta_trans):
    df_limpios = pd.read_csv(ruta_trans)
    print(f"Transacciones listas para DW: {len(df_limpios)}")
else:
    print(f"Archivo no encontrado: {ruta_trans}")

ruta_cli = 'clientes_limpios.csv'
if os.path.exists(ruta_cli):
    df_cli_limpios = pd.read_csv(ruta_cli)
    print(f"Clientes listos para DW: {len(df_cli_limpios)}")
else:
    print(f"Archivo no encontrado: {ruta_cli}")

print("\nValidacion terminada.\n")