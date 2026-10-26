import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo gráfico
sns.set_theme(style="whitegrid")

# 1. Cargar el dataset unificado
print("Cargando datos unificados...")
df = pd.read_csv("calendar_unificado.csv")

# 2. Preprocesamiento Temporal y Limpieza
print("Transformando variables y fechas...")
df['date'] = pd.to_datetime(df['date'])

# Extracción de características del tiempo
df['mes_num'] = df['date'].dt.month
df['mes_nombre'] = df['date'].dt.strftime('%B')
df['dia_semana'] = df['date'].dt.strftime('%A')

# Identificar si está ocupado (f = false / no disponible = está reservado)
# 1 si está reservado/ocupado, 0 si está libre/disponible
df['esta_ocupado'] = df['available'].map({'t': 0, 'f': 1})

# Limpieza estricta de la columna precio (eliminar '$' y ',' y convertir a float)
df['price'] = df['price'].astype(str).str.replace(r'[\$,]', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Rellenar nulos de precio (Airbnb no muestra precio en calendar si el día ya está reservado)
# Usamos la media del precio de ese alojamiento específico en esa ciudad
df['price'] = df['price'].fillna(df.groupby(['ciudad', 'listing_id'])['price'].transform('mean'))


# ==========================================
# 3. ANÁLISIS VISUAL MULTICIUDAD
# ==========================================
print("Generando gráficos comparativos...")

# Gráfico 1: Evolución del Precio Promedio por Mes y Ciudad
plt.figure(figsize=(12, 6))
# Ordenamos cronológicamente los meses
orden_meses = df.sort_values('mes_num')['mes_nombre'].unique()

sns.lineplot(
    data=df, 
    x='mes_nombre', 
    y='price', 
    hue='ciudad', 
    order=orden_meses,
    estimator='mean', 
    errorbar=None, 
    marker='o', 
    linewidth=2.5
)
plt.title('Estacionalidad del Precio Promedio por Mes y Ciudad', fontsize=14, pad=15)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Precio Promedio ($)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Ciudades')
plt.tight_layout()
plt.savefig('calendar_1_precios_mensuales.png', dpi=300)
plt.show()

# Gráfico 2: Porcentaje de Ocupación por Ciudad (¿Qué ciudades se llenan más?)
plt.figure(figsize=(10, 5))
# El promedio de la columna 'esta_ocupado' (0 y 1) nos da la tasa de ocupación
sns.barplot(
    data=df, 
    x='ciudad', 
    y='esta_ocupado', 
    estimator='mean', 
    palette='muted', 
    errorbar=None
)
plt.title('Tasa de Ocupación Promedio por Ciudad', fontsize=14, pad=15)
plt.xlabel('Ciudad', fontsize=12)
plt.ylabel('% de Días Ocupados', fontsize=12)
# Multiplicamos el eje Y de 0-1 a 0-100 para que se lea como porcentaje real
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}%'.format(y*100)))
plt.tight_layout()
plt.savefig('calendar_2_tasa_ocupacion.png', dpi=300)
plt.show()

# Gráfico 3: Efecto Fin de Semana (Precios por Día de la Semana)
plt.figure(figsize=(12, 6))
orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

sns.barplot(
    data=df, 
    x='dia_semana', 
    y='price', 
    hue='ciudad', 
    order=orden_dias,
    estimator='mean', 
    errorbar=None
)
plt.title('Impacto del Fin de Semana en los Precios', fontsize=14, pad=15)
plt.xlabel('Día de la Semana', fontsize=12)
plt.ylabel('Precio Promedio ($)', fontsize=12)
plt.legend(title='Ciudades')
plt.tight_layout()
plt.savefig('calendar_3_efecto_finde.png', dpi=300)
plt.show()

print("\n¡Todo listo! Archivos procesados y gráficos multiciudad guardados localmente.")
