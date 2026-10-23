import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
SERVER = os.getenv('DB_SERVER')
DRIVER = os.getenv('DB_DRIVER')

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
    conn_dw = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=DataRetail360_DW;Trusted_connection=yes;', autocommit=True)
    cursor_dw = conn_dw.cursor()
    
    print("Vaciando tablas de hechos y logs...")
    tablas_a_vaciar = ["fact_ventas", "fact_ventas_staging", "etl_log_ejecucion", "tabla_rechazos"]
    for tabla in tablas_a_vaciar:
        cursor_dw.execute(f"DELETE FROM {tabla};")
        
    cursor_dw.close()
    conn_dw.close()
    print("Base de datos DataRetail360_DW purgada (dimensiones intactas).")
except Exception as e:
    print(f"Error al limpiar DataRetail360_DW: {e}")

print("Eliminando archivos temporales...")
archivos_csv = ['datos_crudos.csv', 'datos_limpios.csv', 'clientes_crudos.csv', 'clientes_limpios.csv', 'resumen_rechazos.csv']
for archivo in archivos_csv:
    if os.path.exists(archivo):
        os.remove(archivo)
        print(f"Archivo {archivo} eliminado.")
    else:
        print(f"Archivo {archivo} no existe.")

print("Terminado.")