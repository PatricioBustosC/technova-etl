import pandas as pd
import pyodbc
import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')
conn_dw_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=technova_dw;Trusted_connection=yes;'

print("Iniciando carga en technova_dw...")
conn = pyodbc.connect(conn_dw_str, autocommit=True)
cursor = conn.cursor()

print("Cargando tabla rechazos...")
cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='rechazos' AND xtype='U')
    CREATE TABLE rechazos (
        id_rechazo INT IDENTITY(1,1) PRIMARY KEY,
        cantidad INT NOT NULL,
        razon VARCHAR(255) NOT NULL,
        fecha_proceso DATETIME DEFAULT GETDATE()
    )
""")

if os.path.exists('resumen_rechazos.csv'):
    df_rechazos = pd.read_csv('resumen_rechazos.csv')
    for index, row in df_rechazos.iterrows():
        cursor.execute("INSERT INTO rechazos (cantidad, razon) VALUES (?, ?)", int(row['cantidad']), str(row['razon']))
    print(f"Rechazos insertados: {len(df_rechazos)}")

print("Cargando dimension cliente...")
if os.path.exists('clientes_limpios.csv'):
    df_clientes = pd.read_csv('clientes_limpios.csv')
    for index, row in df_clientes.iterrows():
        rut = str(row['rut'])[:12]
        nombre = str(row['nombre_cliente'])[:100] if pd.notna(row['nombre_cliente']) else 'Desconocido'
        email = str(row['email'])[:100] if pd.notna(row['email']) else None
        segmento = str(row['segmento'])[:50] if pd.notna(row['segmento']) else 'Sin Asignar'
        
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM dim_cliente WHERE rut = ?)
            INSERT INTO dim_cliente (rut, nombre_cliente, email, segmento)
            VALUES (?, ?, ?, ?)
        """, rut, rut, nombre, email, segmento)
    print(f"Clientes procesados: {len(df_clientes)}")
else:
    print("Error: Archivo clientes_limpios.csv no encontrado.")

print("Cargando otras dimensiones y hechos...")
if os.path.exists('datos_limpios.csv'):
    df_limpios = pd.read_csv('datos_limpios.csv')
    
    def parse_date(val):
        try:
            return pd.to_datetime(val).strftime('%Y-%m-%d')
        except:
            return '2026-10-01'

    for index, row in df_limpios.iterrows():
        id_venta = int(str(row['id_transaccion']).replace('LOG-', ''))
        rut = str(row['rut'])[:12]
        sku = str(row['sku'])[:50]
        tienda_id = int(float(row['tienda']))
        canal = str(row['canal'])[:50] if pd.notna(row['canal']) else 'Desconocido'
        fecha_str = parse_date(row['fecha'])
        cantidad = int(row['cantidad'])
        monto = float(row['monto'])
        
        cursor.execute("IF NOT EXISTS (SELECT 1 FROM dim_cliente WHERE rut = ?) INSERT INTO dim_cliente (rut, nombre_cliente) VALUES (?, 'Cliente Desconocido')", rut, rut)
        
        cursor.execute("IF NOT EXISTS (SELECT 1 FROM dim_producto WHERE sku = ?) INSERT INTO dim_producto (sku, nombre_producto) VALUES (?, 'Producto TNR')", sku, sku)
        cursor.execute("IF NOT EXISTS (SELECT 1 FROM dim_tienda WHERE id_tienda = ?) INSERT INTO dim_tienda (id_tienda, nombre_tienda) VALUES (?, 'Tienda TNR')", tienda_id, tienda_id)
        
        canal_id = abs(hash(canal)) % 1000
        cursor.execute("IF NOT EXISTS (SELECT 1 FROM dim_canal_venta WHERE id_canal = ?) INSERT INTO dim_canal_venta (id_canal, nombre_canal) VALUES (?, ?)", canal_id, canal_id, canal)
        
        tiempo_id = int(fecha_str.replace('-', ''))
        anio, mes, dia = int(fecha_str[:4]), int(fecha_str[5:7]), int(fecha_str[8:10])
        cursor.execute("IF NOT EXISTS (SELECT 1 FROM dim_tiempo WHERE id_tiempo = ?) INSERT INTO dim_tiempo (id_tiempo, fecha, anio, mes, dia, trimestre) VALUES (?, ?, ?, ?, ?, 4)", tiempo_id, tiempo_id, fecha_str, anio, mes, dia)
        
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM fact_ventas WHERE id_venta = ?)
            INSERT INTO fact_ventas (id_venta, rut, sku, id_tienda, id_canal, id_tiempo, cantidad, monto_total, estado_venta)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Activa')
        """, id_venta, id_venta, rut, sku, tienda_id, canal_id, tiempo_id, cantidad, monto)

    print(f"Transacciones procesadas: {len(df_limpios)}")
else:
    print("Error: Archivo datos_limpios.csv no encontrado.")

conn.close()
print("Proceso terminado.")