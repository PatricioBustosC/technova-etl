import pyodbc
import pandas as pd
import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')
conn_dw_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DataRetail360_DW;Trusted_connection=yes;'

print("\nConsultando DataRetail360_DW...\n")

query_clientes = "SELECT cliente_id, nombre, comuna, region, segmento FROM dim_cliente;"

query_ventas = """
SELECT 
    f.venta_id,
    f.num_boleta,
    c.nombre AS nombre_cliente,
    p.producto,
    s.sucursal,
    cn.canal,
    f.cantidad,
    f.monto_neto
FROM fact_ventas f
JOIN dim_cliente c ON f.cliente_key = c.cliente_key
JOIN dim_producto p ON f.producto_key = p.producto_key
JOIN dim_sucursal s ON f.sucursal_key = s.sucursal_key
JOIN dim_canal cn ON f.canal_key = cn.canal_key
ORDER BY f.venta_id;
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