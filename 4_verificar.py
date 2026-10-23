import pyodbc
import pandas as pd
import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')

print("\nREPORTE DE AUDITORIA (ETL)\n")

try:
    conn_sucia = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DB_SUCIA;Trusted_connection=yes;')
    df_sucia_trans = pd.read_sql("SELECT COUNT(*) as total FROM transacciones_sucias", conn_sucia)
    df_sucia_cli = pd.read_sql("SELECT COUNT(*) as total FROM cliente_sucio", conn_sucia)
    print("1. FUENTE ORIGEN (DB_SUCIA)")
    print(f"Transacciones extraidas: {df_sucia_trans.iloc[0]['total']}")
    print(f"Clientes extraidos: {df_sucia_cli.iloc[0]['total']}\n")
    conn_sucia.close()
except Exception as e:
    print(f"Error DB_SUCIA: {e}")

try:
    conn_dw = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=technova_dw;Trusted_connection=yes;')
    print("2. RECHAZOS (technova_dw)")
    df_rechazos = pd.read_sql("SELECT id_rechazo, cantidad, razon FROM rechazos", conn_dw)
    
    if df_rechazos.empty:
        print("Sin registros de rechazo.\n")
    else:
        print(df_rechazos.to_string(index=False))
        print("\n")
    conn_dw.close()
except Exception as e:
    print(f"Error technova_dw: {e}")

print("3. DATOS LIMPIOS")
ruta_trans = 'datos_limpios.csv'
if os.path.exists(ruta_trans):
    df_limpios = pd.read_csv(ruta_trans)
    print(f"Transacciones listas: {len(df_limpios)}")
else:
    print(f"Archivo no encontrado: {ruta_trans}")

ruta_cli = 'clientes_limpios.csv'
if os.path.exists(ruta_cli):
    df_cli_limpios = pd.read_csv(ruta_cli)
    print(f"Clientes listos: {len(df_cli_limpios)}")
else:
    print(f"Archivo no encontrado: {ruta_cli}")

print("\nValidacion terminada.\n")