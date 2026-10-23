import pyodbc
import pandas as pd
import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')
conn_dw_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=technova_dw;Trusted_connection=yes;'

print("\nConsultando technova_dw...\n")

query_clientes = "SELECT rut, nombre_cliente, email, segmento FROM dim_cliente;"

query_ventas = """
SELECT 
    f.id_venta,
    f.rut,
    p.nombre_producto,
    t.nombre_tienda,
    cv.nombre_canal,
    f.cantidad,
    f.monto_total,
    f.estado_venta
FROM fact_ventas f
JOIN dim_producto p ON f.sku = p.sku
JOIN dim_tienda t ON f.id_tienda = t.id_tienda
JOIN dim_canal_venta cv ON f.id_canal = cv.id_canal
ORDER BY f.id_venta;
"""

try:
    conn = pyodbc.connect(conn_dw_str)
    
    print("--- TABLA DE CLIENTES (dim_cliente) ---")
    df_clientes = pd.read_sql(query_clientes, conn)
    if df_clientes.empty:
        print("La tabla de clientes esta vacia.\n")
    else:
        print(df_clientes.to_string(index=False))
        print(f"\nTotal clientes: {len(df_clientes)}\n")

    print("--- TABLA DE VENTAS (fact_ventas) ---")
    df_ventas = pd.read_sql(query_ventas, conn)
    if df_ventas.empty:
        print("La tabla de ventas esta vacia.\n")
    else:
        print(df_ventas.to_string(index=False))
        print(f"\nTotal ventas mostradas: {len(df_ventas)}\n")
        
    conn.close()
except Exception as e:
    print(f"Error de consulta: {e}")