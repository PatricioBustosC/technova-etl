import pyodbc
import os

SERVER = '127.0.0.1'
DRIVER = '{ODBC Driver 17 for SQL Server}'

print("🧹 Iniciando protocolo de limpieza extrema para la presentación...")

# 1. Eliminar DB_SUCIA
try:
    conn_master = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};Trusted_connection=yes;', autocommit=True)
    cursor_master = conn_master.cursor()
    print("🔥 Destruyendo la base de datos 'DB_SUCIA'...")
    cursor_master.execute("""
        IF EXISTS (SELECT * FROM sys.databases WHERE name = 'DB_SUCIA')
        BEGIN
            ALTER DATABASE DB_SUCIA SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
            DROP DATABASE DB_SUCIA;
        END
    """)
    cursor_master.close()
    conn_master.close()
    print("   ➔ DB_SUCIA eliminada sin dejar rastro.")
except Exception as e:
    print(f"❌ Error al intentar borrar DB_SUCIA: {e}")

# 2. Vaciar technova_dw
try:
    conn_dw = pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE=technova_dw;Trusted_connection=yes;', autocommit=True)
    cursor_dw = conn_dw.cursor()
    
    print("🗑️ Borrando la tabla 'rechazos'...")
    cursor_dw.execute("IF EXISTS (SELECT * FROM sysobjects WHERE name='rechazos' AND xtype='U') DROP TABLE rechazos;")
    
    print("🌪️ Vaciando tabla de hechos y dimensiones...")
    tablas_a_vaciar = ["fact_ventas", "dim_cliente", "dim_producto", "dim_tienda", "dim_canal_venta", "dim_tiempo"]
    for tabla in tablas_a_vaciar:
        cursor_dw.execute(f"DELETE FROM {tabla};")
        
    cursor_dw.close()
    conn_dw.close()
    print("   ➔ Base de datos technova_dw purgada.")
except Exception as e:
    print(f"❌ Error al intentar limpiar technova_dw: {e}")

# 3. Eliminar archivos CSV locales
print("📁 Limpiando archivos temporales CSV...")
archivos_csv = ['datos_crudos.csv', 'datos_limpios.csv', 'resumen_rechazos.csv']
for archivo in archivos_csv:
    if os.path.exists(archivo):
        os.remove(archivo)
        print(f"   ➔ Archivo '{archivo}' eliminado.")
    else:
        print(f"   ➔ El archivo '{archivo}' ya no existe.")

print("\n✨ ¡Todo limpio y purificado! Tu entorno está listo para sacarte ese 7.")