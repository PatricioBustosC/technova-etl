import pyodbc
import os

SERVER = '127.0.0.1'
DRIVER = '{ODBC Driver 17 for SQL Server}'

print("Iniciando limpieza del entorno...")

try:
    conn_master = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};Trusted_connection=yes;', autocommit=True)
    cursor_master = conn_master.cursor()
    print("Eliminando base de datos DB_SUCIA...")
    cursor_master.execute("""
        IF EXISTS (SELECT * FROM sys.databases WHERE name = 'DB_SUCIA')
        BEGIN
            ALTER DATABASE DB_SUCIA SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
            DROP DATABASE DB_SUCIA;
        END
    """)
    cursor_master.close()
    conn_master.close()
    print("DB_SUCIA eliminada.")
except Exception as e:
    print(f"Error al borrar DB_SUCIA: {e}")

try:
    conn_dw = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=technova_dw;Trusted_connection=yes;', autocommit=True)
    cursor_dw = conn_dw.cursor()
    
    print("Eliminando tabla rechazos...")
    cursor_dw.execute("IF EXISTS (SELECT * FROM sysobjects WHERE name='rechazos' AND xtype='U') DROP TABLE rechazos;")
    
    print("Vaciando tablas...")
    tablas_a_vaciar = ["fact_ventas", "dim_cliente", "dim_producto", "dim_tienda", "dim_canal_venta", "dim_tiempo"]
    for tabla in tablas_a_vaciar:
        cursor_dw.execute(f"DELETE FROM {tabla};")
        
    cursor_dw.close()
    conn_dw.close()
    print("Base de datos purgada.")
except Exception as e:
    print(f"Error al limpiar technova_dw: {e}")

print("Eliminando archivos temporales...")
archivos_csv = ['datos_crudos.csv', 'datos_limpios.csv', 'resumen_rechazos.csv']
for archivo in archivos_csv:
    if os.path.exists(archivo):
        os.remove(archivo)
        print(f"Archivo {archivo} eliminado.")
    else:
        print(f"Archivo {archivo} no existe.")

print("Terminado.")