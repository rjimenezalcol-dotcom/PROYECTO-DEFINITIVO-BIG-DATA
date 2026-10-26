import os
import pandas as pd

# 1. Definir la ruta base donde están las carpetas de las ciudades
# Estructura esperada: ./datos/madrid/reviews.csv, ./datos/barcelona/reviews.csv, etc.
RUTA_DATOS = "datos/"  
ciudades = [f for f in os.listdir(RUTA_DATOS) if os.path.isdir(os.path.join(RUTA_DATOS, f))]

lista_reviews = []

print("--- Iniciando la unificación de Reviews ---")

for ciudad in ciudades:
    ruta_archivo = os.path.join(RUTA_DATOS, ciudad, "reviews.csv")
    
    if os.path.exists(ruta_archivo):
        print(f"Procesando opiniones de: {ciudad}...")
        
        # Leemos el dataset de la ciudad
        df_temp = pd.read_csv(ruta_archivo)
        
        # OBLIGATORIO: Añadir columna de ciudad para el análisis comparativo posterior
        df_temp['ciudad'] = ciudad.capitalize()
        
        # Opcional: Nos quedamos solo con las columnas clave para optimizar la memoria
        columnas_interes = ['listing_id', 'id', 'date', 'reviewer_id', 'reviewer_name', 'comments', 'ciudad']
        columnas_validas = [c for c in columnas_interes if c in df_temp.columns]
        df_temp = df_temp[columnas_validas]
        
        lista_reviews.append(df_temp)
    else:
        print(f"⚠️ No se encontró reviews.csv en la carpeta: {ciudad}")

# 2. Concatenar todos los DataFrames en uno solo
if lista_reviews:
    reviews_unificado = pd.concat(lista_reviews, ignore_index=True)
    
    # Guardar el resultado final
    archivo_salida = "reviews_unificado.csv"
    reviews_unificado.to_csv(archivo_salida, index=False)
    print(f"\n¡Éxito! Archivo guardado como '{archivo_salida}' con {reviews_unificado.shape} opiniones unificadas.")
else:
    print("\n❌ Error: No se pudo encontrar ni unificar ningún archivo de reviews.")
