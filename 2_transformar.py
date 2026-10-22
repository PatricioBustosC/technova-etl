import pandas as pd

print("⚙️ Iniciando limpieza de datos...")
df = pd.read_csv('datos_crudos.csv')
rechazos_log = []

# 1. Limpiar Nulos (incluyendo textos que significan nulo)
df['tienda'] = df['tienda'].astype(str).str.strip().replace(['nan', 'None', 'Sin Asignar', 'N/A', ''], None)
nulos_mask = df.isnull().any(axis=1)
cant_nulos = nulos_mask.sum()
if cant_nulos > 0:
    rechazos_log.append({'cantidad': cant_nulos, 'razon': 'Contiene valores nulos o sin asignar'})
df = df[~nulos_mask]

# 2. Limpiar Valores Negativos (en cantidad o monto)
negativos_mask = (df['cantidad'] < 0) | (df['monto'] < 0)
cant_negativos = negativos_mask.sum()
if cant_negativos > 0:
    rechazos_log.append({'cantidad': cant_negativos, 'razon': 'Valor negativo en cantidad o monto'})
df = df[~negativos_mask]

# 3. Limpiar Duplicados (dejando solo 1)
# Nos basamos en RUT, SKU, fecha, cantidad y monto para detectar la misma transacción
duplicados_mask = df.duplicated(subset=['rut', 'sku', 'fecha', 'cantidad', 'monto'], keep='first')
cant_duplicados = duplicados_mask.sum()
if cant_duplicados > 0:
    rechazos_log.append({'cantidad': cant_duplicados, 'razon': 'Registro duplicado exacto'})
df = df[~duplicados_mask]

# Guardar resultados
df.to_csv('datos_limpios.csv', index=False)
df_rechazos = pd.DataFrame(rechazos_log)
df_rechazos.to_csv('resumen_rechazos.csv', index=False)

print(f"✅ Transformación lista. Quedaron {len(df)} registros limpios.")
print("📊 Resumen de rechazos generados:")
print(df_rechazos)