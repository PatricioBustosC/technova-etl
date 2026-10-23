import pandas as pd
import pyodbc
import os
import warnings
import re
from dotenv import load_dotenv

warnings.filterwarnings('ignore', category=UserWarning)

load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')
conn_str = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DataRetail360_DW;Trusted_connection=yes;'

print("Iniciando carga en DataRetail360_DW...")
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()


cursor.execute("""
    INSERT INTO etl_log_ejecucion (nombre_paquete, fecha_inicio, estado) 
    VALUES ('Pipeline_Python_Ventas', GETDATE(), 'EN PROCESO')
""")
cursor.execute("SELECT @@IDENTITY")
log_id = cursor.fetchone()[0]

filas_cargadas = 0
filas_rechazadas = 0

try:

    if os.path.exists('resumen_rechazos.csv'):
        df_rechazos = pd.read_csv('resumen_rechazos.csv')
        for index, row in df_rechazos.iterrows():
            cursor.execute("""
                INSERT INTO tabla_rechazos (origen, campo_erroneo, motivo_rechazo) 
                VALUES ('Python_ETL', 'Múltiples', ?)
            """, str(row['razon']))
        filas_rechazadas = len(df_rechazos)
        print(f"Rechazos registrados: {filas_rechazadas}")


    if os.path.exists('clientes_limpios.csv'):
        print("Cargando clientes a dim_cliente...")
        df_clientes = pd.read_csv('clientes_limpios.csv')
        for index, row in df_clientes.iterrows():
            cid = str(row['cliente_id'])
            nombre = str(row['nombre'])[:150] if pd.notna(row['nombre']) else 'Cliente Desconocido'
            comuna = str(row['comuna'])[:100] if pd.notna(row['comuna']) else 'Desconocida'
            region = str(row['region'])[:100] if pd.notna(row['region']) else 'Desconocida'
            segmento = str(row['segmento'])[:50] if pd.notna(row['segmento']) else 'General'
            
            cursor.execute("SELECT cliente_key FROM dim_cliente WHERE cliente_id = ?", cid)
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO dim_cliente (cliente_id, nombre, comuna, region, segmento, valido_desde, es_actual)
                    VALUES (?, ?, ?, ?, ?, GETDATE(), 1)
                """, cid, nombre, comuna, region, segmento)


    if os.path.exists('datos_limpios.csv'):
        df_limpios = pd.read_csv('datos_limpios.csv')
        
        print("Limpiando tabla staging...")
        cursor.execute("TRUNCATE TABLE fact_ventas_staging")
        
        print("Subiendo datos a staging (con validación de llaves)...")
        for index, row in df_limpios.iterrows():
       
            fecha_str = str(row['fecha_transaccion'])
            fecha_clean = re.sub(r'[^0-9]', '', fecha_str)
            fecha_key = int(fecha_clean[:8]) if len(fecha_clean) >= 8 else 20250115
            
     
            cursor.execute("SELECT 1 FROM dim_fecha WHERE fecha_key = ?", fecha_key)
            if not cursor.fetchone():
                try:
                    s_f = str(fecha_key)
                    anio, mes, dia = int(s_f[:4]), int(s_f[4:6]), int(s_f[6:8])
                    if 1 <= mes <= 12 and 1 <= dia <= 31:
                        trimestre = (mes - 1) // 3 + 1
                        nombres_mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                        fecha_real = f"{anio}-{mes:02d}-{dia:02d}"
                        cursor.execute("""
                            INSERT INTO dim_fecha (fecha_key, fecha, dia, mes, nombre_mes, trimestre, anio, es_feriado)
                            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                        """, fecha_key, fecha_real, dia, mes, nombres_mes[mes-1], trimestre, anio)
                    else:
                        fecha_key = 20250115
                except Exception:
                    fecha_key = 20250115 
            # -----------------------------------------------------------

            cantidad = int(row['cantidad'])
            monto = float(row['monto_neto'])
            boleta = str(row['num_boleta'])
            

            cursor.execute("SELECT producto_key FROM dim_producto WHERE sku = ?", str(row['sku']))
            prod_res = cursor.fetchone()
            producto_key = prod_res[0] if prod_res else 999
            
            cursor.execute("SELECT sucursal_key FROM dim_sucursal WHERE codigo_sucursal = ?", str(row['codigo_sucursal']))
            suc_res = cursor.fetchone()
            sucursal_key = suc_res[0] if suc_res else 999
            
            cursor.execute("SELECT canal_key FROM dim_canal WHERE codigo_canal = ?", str(row['codigo_canal']))
            can_res = cursor.fetchone()
            canal_key = can_res[0] if can_res else 1
            
            cursor.execute("SELECT cliente_key FROM dim_cliente WHERE cliente_id = ?", str(row['cliente_id']))
            cli_res = cursor.fetchone()
            cliente_key = cli_res[0] if cli_res else 999
            
            cursor.execute("""
                INSERT INTO fact_ventas_staging 
                (fecha_key, producto_key, sucursal_key, canal_key, cliente_key, num_boleta, cantidad, monto_neto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, fecha_key, producto_key, sucursal_key, canal_key, cliente_key, boleta, cantidad, monto)
        

        print("Ejecutando MERGE hacia fact_ventas...")
        cursor.execute("""
            MERGE INTO fact_ventas AS destino
            USING fact_ventas_staging AS origen
            ON destino.num_boleta = origen.num_boleta
            WHEN MATCHED THEN
                UPDATE SET cantidad = origen.cantidad, monto_neto = origen.monto_neto
            WHEN NOT MATCHED THEN
                INSERT (fecha_key, producto_key, sucursal_key, canal_key, cliente_key, num_boleta, cantidad, monto_bruto, monto_neto, es_devolucion)
                VALUES (origen.fecha_key, origen.producto_key, origen.sucursal_key, origen.canal_key, origen.cliente_key, origen.num_boleta, origen.cantidad, origen.monto_neto, origen.monto_neto, 0);
        """)
        
        filas_cargadas = len(df_limpios)
        print(f"Transacciones procesadas exitosamente: {filas_cargadas}")


    cursor.execute("""
        UPDATE etl_log_ejecucion 
        SET fecha_fin = GETDATE(), filas_cargadas = ?, filas_rechazadas = ?, estado = 'EXITOSO'
        WHERE log_id = ?
    """, filas_cargadas, filas_rechazadas, log_id)

except Exception as e:

    cursor.execute("""
        UPDATE etl_log_ejecucion 
        SET fecha_fin = GETDATE(), estado = 'ERROR', mensaje_error = ?
        WHERE log_id = ?
    """, str(e)[:4000], log_id)
    print(f"Error en el proceso: {e}")

conn.close()
print("Proceso terminado.")