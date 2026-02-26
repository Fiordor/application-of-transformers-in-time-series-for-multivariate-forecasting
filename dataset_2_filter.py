import pandas as pd

# Cargar el dataset generado
df = pd.read_csv("dataset_mercado_continuo_20y.csv")
df['ds'] = pd.to_datetime(df['ds'])

# Agrupar por empresa y sacar métricas
stats = df.groupby('unique_id').agg(
    start_date=('ds', 'min'),
    end_date=('ds', 'max'),
    count=('ds', 'count')
).reset_index()

# Definir criterios de "Superviviente Completo"
# Por ejemplo: Que empiece antes de 2005 y termine en 2024
FECHA_CORTE_INICIO = pd.Timestamp("2005-01-01")
FECHA_CORTE_FIN = pd.Timestamp("2024-01-01")

survivors = stats[
    (stats['start_date'] < FECHA_CORTE_INICIO) & 
    (stats['end_date'] > FECHA_CORTE_FIN)
]

dead = stats[stats['end_date'] < FECHA_CORTE_FIN]
newcomers = stats[stats['start_date'] > FECHA_CORTE_INICIO]

print(f"Total empresas analizadas: {len(stats)}")
print(f"✅ Supervivientes (20 años completos): {len(survivors)}")
print(f"💀 Desaparecidas/Excluidas (Detectadas): {len(dead)}")
print(f"👶 Recién llegadas (No tienen 20 años): {len(newcomers)}")

print("\nEjemplo de Supervivientes:")
print(survivors['unique_id'].head(10).tolist())