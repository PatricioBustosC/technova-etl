import pandas as pd

print("Iniciando transformacion...")
rechazos_log = []

df_trans = pd.read_csv('datos_crudos.csv')

df_trans['codigo_sucursal'] = df_trans['codigo_sucursal'].astype(str).str.strip().replace(['nan', 'None', 'Sin Asignar', 'N/A', ''], None)
nulos_mask = df_trans.isnull().any(axis=1)
cant_nulos = nulos_mask.sum()
if cant_nulos > 0:
    rechazos_log.append({'cantidad': cant_nulos, 'razon': 'Valores nulos en transacciones'})
df_trans = df_trans[~nulos_mask]

negativos_mask = (df_trans['cantidad'] < 0) | (df_trans['monto_neto'] < 0)
cant_negativos = negativos_mask.sum()
if cant_negativos > 0:
    rechazos_log.append({'cantidad': cant_negativos, 'razon': 'Valores negativos en transacciones'})
df_trans = df_trans[~negativos_mask]

duplicados_mask = df_trans.duplicated(subset=['cliente_id', 'sku', 'fecha_transaccion', 'cantidad', 'monto_neto'], keep='first')
cant_duplicados = duplicados_mask.sum()
if cant_duplicados > 0:
    rechazos_log.append({'cantidad': cant_duplicados, 'razon': 'Duplicados en transacciones'})
df_trans = df_trans[~duplicados_mask]

df_trans.to_csv('datos_limpios.csv', index=False)

df_clientes = pd.read_csv('clientes_crudos.csv')

df_clientes['cliente_id'] = df_clientes['cliente_id'].astype(str).str.strip()

nulos_clientes = df_clientes.isnull().any(axis=1)
cant_nulos_clientes = nulos_clientes.sum()
if cant_nulos_clientes > 0:
    rechazos_log.append({'cantidad': cant_nulos_clientes, 'razon': 'Valores nulos en clientes'})
df_clientes = df_clientes[~nulos_clientes]

duplicados_clientes = df_clientes.duplicated(subset=['cliente_id'], keep='first')
cant_duplicados_clientes = duplicados_clientes.sum()
if cant_duplicados_clientes > 0:
    rechazos_log.append({'cantidad': cant_duplicados_clientes, 'razon': 'Duplicados en clientes'})
df_clientes = df_clientes[~duplicados_clientes]

df_clientes.to_csv('clientes_limpios.csv', index=False)

df_rechazos = pd.DataFrame(rechazos_log)
df_rechazos.to_csv('resumen_rechazos.csv', index=False)

print(f"Transformacion terminada. Transacciones limpias: {len(df_trans)} | Clientes limpios: {len(df_clientes)}")
print("Resumen de rechazos:")
print(df_rechazos)