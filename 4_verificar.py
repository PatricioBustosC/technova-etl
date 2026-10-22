import pyodbc
import pandas as pd
import os
import warnings
from dotenv import load_dotenv

# Silenciamos la advertencia roja de SQLAlchemy
warnings.filterwarnings('ignore', category=UserWarning)

# Carga las variables seguras
load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')

print("\n" + "═"*70)
print(" 📊 REPORTE DE AUDITORÍA Y CALIDAD DE DATOS (ETL)".center(70))
print("═"*70 + "\n")

# 1. DB_SUCIA
try:
    conn_sucia = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DB_SUCIA;Trusted_connection=yes;')
    df_sucia = pd.read_sql("SELECT COUNT(*) as total FROM transacciones_sucias", conn_sucia)
    print(f" 📦 1. FUENTE ORIGEN (DB_SUCIA)")
    print(f"    ➔ Total de registros extraídos: {df_sucia.iloc[0]['total']}")
    print("-" * 70)
    conn_sucia.close()
except Exception as e:
    print(f" ❌ Error al conectar con DB_SUCIA: {e}")

# 2. RECHAZOS
try:
    conn_dw = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=technova_dw;Trusted_connection=yes;')
    print(" 🚫 2. AUDITORÍA DE RECHAZOS (technova_dw)")
    df_rechazos = pd.read_sql("SELECT id_rechazo, cantidad, razon, fecha_proceso FROM rechazos", conn_dw)
    
    if df_rechazos.empty:
        print("    ➔ No se encontraron registros de rechazo.")
    else:
        print(f"    ┌──────┬────────────┬────────────────────────────────────────────┐")
        print(f"    │  ID  │  Cantidad  │ Razón del Rechazo                          │")
        print(f"    ├──────┼────────────┼────────────────────────────────────────────┤")
        for _, row in df_rechazos.iterrows():
            id_r = str(row['id_rechazo']).center(4)
            cant = str(row['cantidad']).center(10)
            razon = str(row['razon']).ljust(42)
            print(f"    │ {id_r} │ {cant} │ {razon} │")
        print(f"    └──────┴────────────┴────────────────────────────────────────────┘")
    print("-" * 70)
    conn_dw.close()
except Exception as e:
    print(f" ❌ Error al conectar con technova_dw: {e}")

# 3. DATOS LIMPIOS
ruta_limpios = 'datos_limpios.csv'
if os.path.exists(ruta_limpios):
    df_limpios = pd.read_csv(ruta_limpios)
    print(f" ✨ 3. RESULTADO FINAL (DATOS LIMPIOS)")
    print(f"    ➔ Registros aprobados y listos: {len(df_limpios)}")
    print(f"    ➔ Archivo generado: '{ruta_limpios}'")
else:
    print(f" ❌ No se encontró el archivo '{ruta_limpios}'.")

print("\n" + "═"*70)
print(" Proceso de validación finalizado con éxito ".center(70))
print("═"*70 + "\n")