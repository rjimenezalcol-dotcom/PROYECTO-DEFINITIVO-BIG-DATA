import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración estética
sns.set_theme(style="whitegrid")

# 1. Carga de datos (Simulado para una ciudad o el unificado de reviews)
# Supongamos que los alumnos ya unificaron las reviews añadiendo la columna 'ciudad'
df_reviews = pd.read_csv('reviews_unificado.csv')

# Limpieza inicial: eliminar comentarios vacíos
df_reviews = df_reviews.dropna(subset=['comments'])
df_reviews['comments'] = df_reviews['comments'].astype(str)

print(f"Dataset de opiniones cargado con {df_reviews.shape[0]} registros.")


# ==========================================
# RETO 1: LONGITUD DE LOS COMENTARIOS
# ==========================================
# Contar cuántas palabras tiene cada comentario
df_reviews['num_palabras'] = df_reviews['comments'].apply(lambda x: len(x.split()))

print("\n--- Estadísticas de longitud de comentarios ---")
print(df_reviews.groupby('ciudad')['num_palabras'].mean().round(1))


# ==========================================
# RETO 2: DETECTOR DE ALERTAS (TEXT MINING)
# ==========================================
# Lista de palabras clave que representan problemas comunes
palabras_alerta = ['sucio', 'ruido', 'malo', 'roto', 'problema', 'cucaracha', 'incómodo']

# Creamos una columna booleana (True/False) si encuentra alguna de las palabras
# Lo pasamos a minúsculas (.lower()) para evitar problemas con mayúsculas
df_reviews['tiene_alerta'] = df_reviews['comments'].str.lower().apply(
    lambda x: any(palabra in x for palabra in palabras_alerta)
)

# Calcular el porcentaje de quejas por ciudad
quejas_por_ciudad = df_reviews.groupby('ciudad')['tiene_alerta'].mean().reset_index()
quejas_por_ciudad['%_quejas'] = quejas_por_ciudad['tiene_alerta'] * 100

# Gráfico de Alertas por Ciudad
plt.figure(figsize=(10, 5))
sns.barplot(data=quejas_por_ciudad, x='ciudad', y='%_quejas', palette='Reds_r')
plt.title('Porcentaje de Opiniones con Palabras de Alerta por Ciudad', fontsize=14, pad=15)
plt.xlabel('Ciudad', fontsize=12)
plt.ylabel('% de Reseñas Críticas', fontsize=12)
plt.tight_layout()
plt.savefig('reviews_1_alertas_ciudad.png', dpi=300)
plt.show()


# ==========================================
# RETO 3: EVOLUCIÓN HISTÓRICA DE LA DEMANDA
# ==========================================
df_reviews['date'] = pd.to_datetime(df_reviews['date'])
df_reviews['mes_nombre'] = df_reviews['date'].dt.strftime('%B')
df_reviews['mes_num'] = df_reviews['date'].dt.month

# Ordenamos cronológicamente los meses
orden_meses = df_reviews.sort_values('mes_num')['mes_nombre'].unique()

# Gráfico de volumen de opiniones por mes
plt.figure(figsize=(12, 5))
sns.countplot(data=df_reviews, x='mes_nombre', hue='ciudad', order=orden_meses, palette='Set2')
plt.title('Histórico de Volumen de Reseñas por Mes (Indicador de Demanda)', fontsize=14, pad=15)
plt.xlabel('Mes del Año', fontsize=12)
plt.ylabel('Cantidad de Reseñas Dejadas', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Ciudades')
plt.tight_layout()
plt.savefig('reviews_2_volumen_mensual.png', dpi=300)
plt.show()

print("\n¡Ejercicio completado! Gráficos de análisis de texto guardados con éxito.")
