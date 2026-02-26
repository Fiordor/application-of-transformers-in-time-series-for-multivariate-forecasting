import pandas as pd

# 1. Cargar el dataset bruto que bajamos antes
# Asegúrate de usar el nombre del archivo que generaste con el script anterior
df = pd.read_csv("dataset_mercado_continuo_20y.csv") 

# Convertir fecha
df['ds'] = pd.to_datetime(df['ds'])

# 2. FILTRO DE SUPERVIVENCIA
# Contamos cuántos días de datos tiene cada empresa
conteos = df.groupby('unique_id')['ds'].count()

# Calculamos el máximo de días posibles (la empresa "perfecta")
max_dias = conteos.max() 
# Aceptamos empresas que tengan al menos el 95% de los datos (por si falló algún día suelto)
umbral = max_dias * 0.95

# Sacamos la lista de los 56 elegidos
empresas_top_56 = conteos[conteos >= umbral].index.tolist()

print(f"Empresas seleccionadas (Supervivientes): {len(empresas_top_56)}")
print(empresas_top_56)

# 3. FILTRADO
df_final = df[df['unique_id'].isin(empresas_top_56)].copy()

# Ordenar escrupulosamente (Fundamental para Transformers)
df_final = df_final.sort_values(by=['unique_id', 'ds'])

# 4. GUARDADO FINAL
df_final.to_csv("dataset_tfm_56_survivors.csv", index=False)