import pyodbc
import pandas as pd
import warnings

# Silenciamos la advertencia roja de SQLAlchemy para mantener limpia la consola
warnings.filterwarnings('ignore', category=UserWarning)

SERVER = '127.0.0.1'
DRIVER = '{ODBC Driver 17 for SQL Server}'
conn_dw_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=technova_dw;Trusted_connection=yes;'

print("\n🔍 Consultando el Modelo Estrella en technova_dw...\n")

# Hacemos un JOIN entre la tabla de hechos y las dimensiones
query = """
SELECT TOP 15
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
    df_resultados = pd.read_sql(query, conn)
    
    if df_resultados.empty:
        print("❌ La tabla de hechos está vacía. Algo falló en la carga.")
    else:
        # Imprimimos la tabla con formato limpio
        print(df_resultados.to_string(index=False))
        print(f"\n✅ Mostrando {len(df_resultados)} registros del cruce exitoso.")
        
    conn.close()
except Exception as e:
    print(f"❌ Error al consultar la base de datos: {e}")