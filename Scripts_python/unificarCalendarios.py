import os
import pandas as pd

# 1. Definir la ruta donde están las carpetas de las ciudades
# Estructura esperada: ./datos/madrid/calendar.csv, ./datos/barcelona/calendar.csv, etc.
RUTA_DATOS = "datos/"  
ciudades = [f for f in os.listdir(RUTA_DATOS) if os.path.isdir(os.path.join(RUTA_DATOS, f))]

lista_calendar = []

print("--- Iniciando la unificación de Calendar ---")

for ciudad in ciudades:
    ruta_archivo = os.path.join(RUTA_DATOS, ciudad, "calendar.csv")
    
    if os.path.exists(ruta_archivo):
        print(f"Procesando: {ciudad}...")
        # Leemos el dataset de la ciudad
        df_temp = pd.read_csv(ruta_archivo)
        
        # OBLIGATORIO: Añadir columna de ciudad para no perder el origen de los datos
        df_temp['ciudad'] = ciudad.capitalize()
        
        lista_calendar.append(df_temp)
    else:
        print(f"⚠️ No se encontró calendar.csv en la carpeta: {ciudad}")

# 2. Concatenar todos los DataFrames en uno solo
if lista_calendar:
    calendar_unificado = pd.concat(lista_calendar, ignore_index=True)
    
    # Guardar el resultado
    archivo_salida = "calendar_unificado.csv"
    calendar_unificado.to_csv(archivo_salida, index=False)
    print(f"\n¡Éxito! Archivo guardado como '{archivo_salida}' con {calendar_unificado.shape[0]} filas.")
else:
    print("\n❌ Error: No se pudo unificar ningún archivo.")
