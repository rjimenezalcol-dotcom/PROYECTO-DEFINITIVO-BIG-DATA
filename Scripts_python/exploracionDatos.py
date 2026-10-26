import pandas as pd
import matplotlib.pyplot as plt

#comentario prueba 13:14
# Cargamos el dataset preprocesado y limpio
#df = pd.read_csv("airbnb_grecia_clean.csv", low_memory=False)
# En lugar de pd.read_csv('datos_limpios.csv') 
url = "https://drive.google.com/drive/u/0/folders/1cswCtiA3Kgu47Pqid6xVn45Rw0WdnNM6
df = pd.read_csv(url)
print("🔍 Dataset cargado. Iniciando batería de consultas de exploración...")
#Comentario para que pueda comprobar que se ha cargado correctamente el archivo git en el lenguaje R

# =====================================================================
# EJERCICIO 1: Top 5 de Alojamientos Más Caros de España
# Muestra cómo ordenar datos y seleccionar columnas específicas para visualización rápida.
# =====================================================================
print("\n📌 1. TOP 5 ALOJAMIENTOS MÁS CAROS EN GRECIA:")
columnas_vista = ['name', 'region_origen', 'price', 'room_type']
top_caros = df.sort_values(by='price', ascending=False)[columnas_vista].head(5)
print(top_caros.to_string(index=False))


# =====================================================================
# EJERCICIO 2: Precio Promedio y Total de Alojamientos por Región
# Enseña el uso fundamental de .groupby() y la agregación de múltiples métricas.
# =====================================================================
print("\n📌 2. RESUMEN DEL MERCADO POR REGIÓN (Precio Promedio y Volumen):")
# 1. Elimina espacios en blanco y caracteres no numéricos si los hubiera (ej: $, €, comas)
df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()

# 2. Convierte la columna a tipo numérico (los valores no válidos se convertirán en NaN)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
resumen_region = df.groupby('region_origen').agg(
    precio_promedio=('price', 'mean'),
    total_alojamientos=('id', 'count')
).sort_values(by='precio_promedio', ascending=False)

# Formateamos el precio a dos decimales para una lectura limpia
resumen_region['precio_promedio'] = resumen_region['precio_promedio'].round(2)
print(resumen_region)


# =====================================================================
# EJERCICIO 3: El Efecto "Superhost"
# Filtrado analítico para comprobar si los Superhosts cobran más o tienen mejores notas.
# =====================================================================
print("\n📌 3. COMPARATIVA: ¿SER SUPERHOST MARCA LA DIFERENCIA?")
# Filtramos solo los que tienen reseñas válidas (puntuación > 0)
df_con_resenas = df[df['review_scores_rating'] > 0]

efecto_superhost = df_con_resenas.groupby('host_is_superhost').agg(
    precio_medio=('price', 'mean'),
    puntuacion_media=('review_scores_rating', 'mean'),
    total_propiedades=('id', 'count')
).round(2)
print(efecto_superhost)


# =====================================================================
# EJERCICIO 4: Filtrado Avanzado Multicriterio (Oportunidades de Inversión)
# Simula una petición real de un inversor: "Busco apartamentos enteros en Madrid, 
# económicos (<80€), con buena puntuación y capacidad para mínimo 4 personas".
# =====================================================================
print("\n📌 4. BÚSQUEDA DE OPORTUNIDADES (Filtro Cruzado Complejo):")
filtros = (
    (df['region_origen'] == 'Atenas') & 
    (df['room_type'] == 'Entire home/apt') & 
    (df['price'] < 80) & 
    (df['accommodates'] >= 4) & 
    (df['review_scores_rating'] >= 4.5)
)
#filtros = (
    #(df['region_origen'] == 'Atenas') & 
    #(df['room_type'] == 'Entire home/apt') & 
    #(df['price'] < 80) & 
    #(df['accommodates'] >= 4) & 
    #(df['review_scores_rating'] >= 4.5)
#)

oportunidades = df[filtros][['name', 'neighbourhood_cleansed', 'price', 'review_scores_rating']]
print(f"🎯 Se han encontrado {len(oportunidades)} opciones que cumplen los requisitos del inversor.")
print(oportunidades.head(5).to_string(index=False))  # Mostramos solo las primeras 5 para no saturar la pantalla


# =====================================================================
# EJERCICIO 5: Distribución del Tipo de Alojamiento por Región (Matriz de Contingencia)
# Muestra cómo cruzar dos variables categóricas usando crosstab, ideal antes de graficar barras apiladas.
# =====================================================================
print("\n📌 5. MATRIZ DE DISTRIBUCIÓN: TIPO DE ALOJAMIENTO POR REGIÓN:")
matriz_tipos = pd.crosstab(df['region_origen'], df['room_type'])
print(matriz_tipos)

# =====================================================================
print("\n📌 6. FILTRADO AVANZADO DE BÚSQUEDA ASEQUIBLE DE OPORTUNIDADES (Oportunidades de alquiler barato):")
# =====================================================================

filtros = (
    (df['region_origen'] == 'Salonica') &
    (df['room_type'] == 'Entire home/apt') &
    (df['price'] < 400) &
    (df['price'] > 50) &
    (df['accommodates'] >= 4) &
    (df['review_scores_rating'] >= 4.5)
)

oportunidades = df.loc[filtros]

print(f"🎯 Se han encontrado {len(oportunidades)} oportunidades.")
print(
    oportunidades[
        ['name', 'neighbourhood_cleansed', 'price',
         'accommodates', 'review_scores_rating']
    ].head(10).to_string(index=False)
)
# =====================================================================
print("\n📌 7. GRAFICOS DE PRECIOS DE HABITACIONES POR CIUDADES (Graficos de ciudades por coste):")
# Muestra el coste de habitaciones por ciudades en gráficos de columnas.
# =====================================================================

import matplotlib.pyplot as plt

# Calculamos el precio medio y el número de alojamientos por región
resumen_precios = (
    df.groupby('region_origen')['price']
    .agg(['mean', 'count'])
    .reindex(['Atenas', 'Creta', 'Egeo', 'Salonica'])
    .dropna()
)

# Mostramos los datos utilizados en el gráfico
print("\nPrecio medio por región:")
print(resumen_precios.round(2))

# Creamos el gráfico de barras
plt.figure(figsize=(10, 6))

barras = plt.bar(
    resumen_precios.index,
    resumen_precios['mean'],
    color=['royalblue', 'seagreen', 'darkorange', 'mediumpurple']
)

plt.title('Precio medio de alojamientos Airbnb por región de Grecia')
plt.xlabel('Región')
plt.ylabel('Precio medio por noche')
plt.bar_label(barras, fmt='%.2f')
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()

# Guardamos el gráfico como imagen
plt.savefig('precios_medios_por_region.png', dpi=150)

# Mostramos el gráfico en pantalla
plt.show()

# =============================================================
# EJERCICIO 8: RANKING DE LAS 10 OPORTUNIDADES MÁS BARATAS
# =============================================================
print("\n📌 8. RANKING DE LAS 10 OPORTUNIDADES MÁS BARATAS EN SALÓNICA")

from matplotlib.patches import Patch

# Mostrar las regiones disponibles para comprobar el nombre exacto
print("\nRegiones disponibles en el dataset:")
print(sorted(df["region_origen"].dropna().astype(str).unique()))

# Aceptar distintas formas de escribir el nombre de Salónica
regiones_salonica = [
    "salonica", "salónica", "thessaloniki", "θεσσαλονίκη"
]

region_normalizada = (
    df["region_origen"].astype(str).str.strip().str.casefold()
)

# Aplicar los filtros para seleccionar las oportunidades
filtros_salonica = (
    region_normalizada.isin(regiones_salonica)
    & (df["room_type"] == "Entire home/apt")
    & (df["price"] > 50)
    & (df["price"] < 400)
    & (df["accommodates"] >= 4)
    & (df["review_scores_rating"] >= 4.5)
)

oportunidades_salonica = df.loc[filtros_salonica].copy()

print(
    f"\nAlojamientos que cumplen los filtros: "
    f"{len(oportunidades_salonica)}"
)

if oportunidades_salonica.empty:
    print(
        "No se han encontrado alojamientos. "
        "Comprueba el nombre de la región mostrado arriba "
        "y los filtros aplicados."
    )

else:
    # Convertir el precio a número y descartar datos inválidos
    oportunidades_salonica["price"] = pd.to_numeric(
        oportunidades_salonica["price"],
        errors="coerce"
    )

    oportunidades_salonica = oportunidades_salonica.dropna(
        subset=["name", "price"]
    )

    oportunidades_salonica = oportunidades_salonica[
        oportunidades_salonica["price"] > 0
    ]

    # Seleccionar los 10 precios más bajos
    top_oportunidades = (
        oportunidades_salonica
        .nsmallest(10, "price")
        .reset_index(drop=True)
    )

    if top_oportunidades.empty:
        print("No hay precios válidos para crear el ranking.")

    else:
        # Crear posiciones del ranking
        top_oportunidades["ranking"] = range(
            1, len(top_oportunidades) + 1
        )

        # Numerar cada alojamiento en el eje vertical
        top_oportunidades["alojamiento_ranking"] = (
            top_oportunidades["ranking"].astype(str)
            + ". "
            + top_oportunidades["name"].astype(str)
        )

        # Verde: puestos 1-3; amarillo: 4-7; rojo: 8-10
        colores = [
            "green" if puesto <= 3
            else "gold" if puesto <= 7
            else "red"
            for puesto in top_oportunidades["ranking"]
        ]

        # Crear el gráfico horizontal
        fig, ax = plt.subplots(figsize=(14, 8))

        barras = ax.barh(
            top_oportunidades["alojamiento_ranking"],
            top_oportunidades["price"],
            color=colores,
            edgecolor="black",
            linewidth=0.6
        )

        # Etiquetar las barras con su precio
        etiquetas = [
            f"{precio:.2f} €"
            for precio in top_oportunidades["price"]
        ]

        ax.bar_label(
            barras,
            labels=etiquetas,
            padding=5
        )

        # Colocar el alojamiento más barato arriba
        ax.invert_yaxis()

        ax.set_title(
            "Ranking de las 10 oportunidades más baratas en Salónica",
            fontsize=14
        )
        ax.set_xlabel("Precio por noche (€)")
        ax.set_ylabel("Ranking y alojamiento")

        ax.grid(axis="x", linestyle="--", alpha=0.4)
        ax.set_axisbelow(True)

        # Espacio a la derecha para las etiquetas
        precio_maximo = top_oportunidades["price"].max()
        ax.set_xlim(
            0,
            precio_maximo * 1.25 if precio_maximo > 0 else 1
        )

        # Leyenda de colores
        leyenda = [
            Patch(
                facecolor="green",
                edgecolor="black",
                label="Puestos 1-3: más económicos"
            ),
            Patch(
                facecolor="gold",
                edgecolor="black",
                label="Puestos 4-7: tramo intermedio"
            ),
            Patch(
                facecolor="red",
                edgecolor="black",
                label="Puestos 8-10: más caros del ranking"
            )
        ]

        ax.legend(handles=leyenda, loc="lower right")
        plt.tight_layout()

        # Guardar el gráfico y mostrarlo
        plt.savefig(
            "ranking_oportunidades_salonica.png",
            dpi=150,
            bbox_inches="tight"
        )
        plt.show()

        # Imprimir el ranking en consola
        print("\nRANKING DE OPORTUNIDADES EN SALÓNICA:")
        print(
            top_oportunidades[
                ["ranking", "name", "price"]
            ].to_string(index=False)
        )

        # Exportar los resultados a CSV
        top_oportunidades.to_csv(
            "ranking_oportunidades_salonica.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print(
            "\nGráfico guardado como "
            "'ranking_oportunidades_salonica.png'"
        )
        print(
            "Ranking exportado como "
            "'ranking_oportunidades_salonica.csv'"
        )

print("\n✅ Exploración finalizada.")

# =============================================================
# EJERCICIO 9: MOSTRAR EL MAPA DEL RANKING TOP 10
# =============================================================

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

print("\n📌 9. MAPA DEL RANKING TOP 10 DE SALÓNICA")

archivo_mapa = "a_wide_infographic_style_map_image_a_clean_cart.png"

if os.path.exists(archivo_mapa):

    imagen = mpimg.imread(archivo_mapa)

    plt.figure(figsize=(16, 10))
    plt.imshow(imagen)
    plt.axis("off")

    plt.title(
        "Europa: ubicación del ranking Top 10 de alojamientos en Salónica",
        fontsize=14
    )

    plt.tight_layout()
    plt.show()

else:
    print("No se encuentra la imagen del mapa.")
    print("Guarda el archivo PNG en la misma carpeta del programa.")


# =============================================================
# EJERCICIO 10: MAPA INTERACTIVO DEL RANKING TOP 10
# =============================================================

print("\n📌 10. MAPA INTERACTIVO DEL TOP 10 EN SALÓNICA")

import pandas as pd
import folium
import re
import webbrowser
from pathlib import Path

# Comprobar que existe el ranking del ejercicio 8
if "top_oportunidades" not in globals() or top_oportunidades.empty:
    print("ERROR: Ejecuta primero el ejercicio 8.")

else:
    # Detectar las columnas de coordenadas
    columnas = {
        str(c).strip().lower(): c for c in df.columns
    }

    col_lat = next(
        (
            columnas[c]
            for c in ["latitude", "lat", "latitud"]
            if c in columnas
        ),
        None
    )

    col_lon = next(
        (
            columnas[c]
            for c in ["longitude", "long", "lon", "longitud"]
            if c in columnas
        ),
        None
    )

    if "id" not in df.columns or col_lat is None or col_lon is None:
        print("ERROR: No se encuentran id, latitude o longitude.")

    else:
        # Convertir las coordenadas del CSV a formato decimal
        def convertir_coordenada(valor, es_latitud=True):
            if pd.isna(valor):
                return float("nan")

            texto = str(valor).strip().replace(",", ".")

            # Conservar coordenadas decimales válidas
            try:
                numero = float(texto)
                limite = 90 if es_latitud else 180

                if abs(numero) <= limite:
                    return numero

            except ValueError:
                pass

            # Intentar corregir valores con puntos separadores
            digitos = re.sub(r"\D", "", texto)

            if len(digitos) < 3:
                return float("nan")

            numero = float(digitos[:2] + "." + digitos[2:])

            limite = 90 if es_latitud else 180

            if abs(numero) <= limite:
                return numero

            return float("nan")

        # Preparar las coordenadas del CSV
        coordenadas = df[["id", col_lat, col_lon]].copy()

        coordenadas.rename(
            columns={
                col_lat: "latitude",
                col_lon: "longitude"
            },
            inplace=True
        )

        coordenadas["latitude"] = coordenadas["latitude"].apply(
            lambda x: convertir_coordenada(x, True)
        )

        coordenadas["longitude"] = coordenadas["longitude"].apply(
            lambda x: convertir_coordenada(x, False)
        )

        # Unificar el tipo del identificador
        coordenadas["id"] = (
            coordenadas["id"].astype(str).str.strip()
        )

        coordenadas.drop_duplicates(
            subset=["id"],
            inplace=True
        )

        ranking = top_oportunidades.copy()

        ranking["id"] = (
            ranking["id"].astype(str).str.strip()
        )

        # Asociar las coordenadas al ranking
        mapa_datos = ranking.drop(
            columns=["latitude", "longitude"],
            errors="ignore"
        ).merge(
            coordenadas,
            on="id",
            how="left"
        )

        # Eliminar coordenadas vacías
        mapa_datos.dropna(
            subset=["latitude", "longitude"],
            inplace=True
        )

        # Validar rangos geográficos
        mapa_datos = mapa_datos[
            mapa_datos["latitude"].between(-90, 90)
            & mapa_datos["longitude"].between(-180, 180)
        ].copy()

        if mapa_datos.empty:
            print("ERROR: No hay coordenadas válidas.")
            print("Comprueba los valores originales del CSV.")

        else:
            # Comprobar las columnas necesarias
            columnas_necesarias = ["ranking", "name", "price"]

            faltantes = [
                c for c in columnas_necesarias
                if c not in mapa_datos.columns
            ]

            if faltantes:
                print("ERROR: Faltan columnas:", faltantes)

            else:
                # Crear el mapa centrado en los alojamientos
                mapa = folium.Map(
                    location=[
                        mapa_datos["latitude"].mean(),
                        mapa_datos["longitude"].mean()
                    ],
                    zoom_start=12,
                    tiles=None
                )

                # Añadir un mapa base alternativo: Stadia Maps
                folium.TileLayer(
                    tiles=(
                        "https://tiles.stadiamaps.com/tiles/"
                        "alidade_smooth/{z}/{x}/{y}{r}.png"
                    ),
                    attr=(
                        '© Stadia Maps, © OpenMapTiles, '
                        '© OpenStreetMap contributors'
                    ),
                    name="Stadia Maps - Alidade Smooth",
                    overlay=False,
                    control=True,
                    max_zoom=20
                ).add_to(mapa)

                      
                # Crear un marcador para cada alojamiento
                for _, fila in mapa_datos.iterrows():
                    puesto = int(fila["ranking"])

                    # Colores según la posición del ranking
                    if puesto <= 3:
                        color = "green"
                    elif puesto <= 7:
                        color = "orange"
                    else:
                        color = "red"

                    nombre = str(fila["name"])

                    precio = pd.to_numeric(
                        fila["price"],
                        errors="coerce"
                    )

                    precio_texto = (
                        f"{precio:.2f} €"
                        if pd.notna(precio)
                        else "No disponible"
                    )

                    # Información de la ventana emergente
                    popup_html = (
                        f"<b>Ranking:</b> {puesto}<br>"
                        f"<b>Alojamiento:</b> {nombre}<br>"
                        f"<b>Precio:</b> {precio_texto}"
                    )

                    folium.Marker(
                        location=[
                            fila["latitude"],
                            fila["longitude"]
                        ],
                        tooltip=f"Puesto {puesto}: {nombre}",
                        popup=folium.Popup(
                            popup_html,
                            max_width=300
                        ),
                        icon=folium.Icon(
                            color=color,
                            icon="home",
                            prefix="fa"
                        )
                    ).add_to(mapa)

                # Ajustar el zoom para incluir los marcadores
                mapa.fit_bounds(
                    [
                        [
                            mapa_datos["latitude"].min(),
                            mapa_datos["longitude"].min()
                        ],
                        [
                            mapa_datos["latitude"].max(),
                            mapa_datos["longitude"].max()
                        ]
                    ]
                )

                # Guardar el mapa en la carpeta del proyecto
                archivo_mapa = Path(
                    r"C:\Users\14\Desktop\datos\mapa_ranking_salonica.html"
                )

                mapa.save(str(archivo_mapa))

                print("Mapa creado correctamente:", archivo_mapa)
                print(
                    "Alojamientos representados:",
                    len(mapa_datos)
                )

               
                # Abrir automáticamente el mapa mediante el servidor local
                import subprocess
                import socket
                import time

                # Carpeta donde está guardado el mapa
                carpeta_proyecto = archivo_mapa.parent

                # Comprobar si el puerto 8000 ya está en uso
                def puerto_disponible(puerto, host="127.0.0.1"):
                    with socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    ) as conexion:
                        return conexion.connect_ex(
                            (host, puerto)
                        ) != 0

                # Iniciar el servidor solo si no está activo
                if puerto_disponible(8000):
                    servidor = subprocess.Popen(
                        [
                            "py",
                            "-m",
                            "http.server",
                            "8000",
                            "--bind",
                            "127.0.0.1",
                            "--directory",
                            str(carpeta_proyecto)
                        ],
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                            if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP")
                            else 0
                    )

                    time.sleep(1)

                # Abrir el mapa a través del servidor local
                url_mapa = (
                    "http://localhost:8000/"
                    + archivo_mapa.name
                )

                print("Servidor local iniciado o ya disponible.")
                print("Abriendo mapa:", url_mapa)

                webbrowser.open(url_mapa)


# =============================================================
# EJERCICIO 11: DETECCIÓN DE ALOJAMIENTOS INFRAVALORADOS
# =============================================================

print(
    "\n📌 11. DETECCIÓN DE ALOJAMIENTOS "
    "POTENCIALMENTE INFRAVALORADOS"
)

import numpy as np

# 1. Comprobar las columnas necesarias
columnas_necesarias = [
    "id", "name", "region_origen",
    "room_type", "price", "accommodates"
]

faltantes = [
    c for c in columnas_necesarias
    if c not in df.columns
]

if faltantes:
    print("ERROR: Faltan columnas:", faltantes)

else:
    # 2. Preparar una copia de los datos
    oportunidades = df.copy()

    oportunidades["price"] = pd.to_numeric(
        oportunidades["price"], errors="coerce"
    )

    oportunidades["accommodates"] = pd.to_numeric(
        oportunidades["accommodates"], errors="coerce"
    )

    # 3. Limpiar los datos esenciales
    oportunidades = oportunidades.dropna(
        subset=[
            "id", "name", "region_origen",
            "room_type", "price", "accommodates"
        ]
    )

    oportunidades = oportunidades[
        (oportunidades["price"] > 0)
        & (oportunidades["accommodates"] > 0)
    ].copy()

    # 4. Agrupar por capacidad
    oportunidades["tramo_capacidad"] = pd.cut(
        oportunidades["accommodates"],
        bins=[0, 2, 4, 6, float("inf")],
        labels=[
            "1-2 huéspedes",
            "3-4 huéspedes",
            "5-6 huéspedes",
            "7 o más huéspedes"
        ]
    )

    # 5. Preparar las valoraciones
    tiene_valoraciones = "review_scores_rating" in oportunidades.columns

    if tiene_valoraciones:
        oportunidades["review_scores_rating"] = pd.to_numeric(
            oportunidades["review_scores_rating"],
            errors="coerce"
        )

    # 6. Calcular el precio mediano de los comparables
    grupos = [
        "region_origen",
        "room_type",
        "tramo_capacidad"
    ]

    referencia = (
        oportunidades.groupby(
            grupos, observed=True
        )["price"]
        .agg(
            precio_mediano_comparable="median",
            numero_comparables="count"
        )
        .reset_index()
    )

    oportunidades = oportunidades.merge(
        referencia,
        on=grupos,
        how="left",
        validate="many_to_one"
    )

    # 7. Calcular el descuento porcentual
    oportunidades["descuento_pct"] = (
        (
            oportunidades["precio_mediano_comparable"]
            - oportunidades["price"]
        )
        / oportunidades["precio_mediano_comparable"]
    ) * 100

    # 8. Criterios de selección
    MIN_COMPARABLES = 5
    DESCUENTO_MINIMO = 20
    VALORACION_MINIMA = 4.5

    filtro = (
        (oportunidades["numero_comparables"] >= MIN_COMPARABLES)
        & (oportunidades["descuento_pct"] >= DESCUENTO_MINIMO)
    )

    if tiene_valoraciones:
        filtro &= (
            oportunidades["review_scores_rating"].notna()
            & (
                oportunidades["review_scores_rating"]
                >= VALORACION_MINIMA
            )
        )

    infravalorados = oportunidades.loc[filtro].copy()

    # 9. Ordenar y asignar posiciones
    infravalorados = infravalorados.sort_values(
        "descuento_pct",
        ascending=False
    ).reset_index(drop=True)

    infravalorados.insert(
        0,
        "ranking_oportunidad",
        range(1, len(infravalorados) + 1)
    )

    # 10. Mostrar resultados
    columnas_salida = [
        "ranking_oportunidad",
        "id",
        "name",
        "region_origen",
        "room_type",
        "accommodates",
        "price",
        "precio_mediano_comparable",
        "descuento_pct",
        "numero_comparables"
    ]

    if tiene_valoraciones:
        columnas_salida.append("review_scores_rating")

    print("\nALOJAMIENTOS POTENCIALMENTE INFRAVALORADOS")
    print("Total detectado:", len(infravalorados))

    if infravalorados.empty:
        print(
            "No se han encontrado alojamientos que cumplan "
            "todos los criterios establecidos."
        )
    else:
        print(
            infravalorados[columnas_salida]
            .head(20)
            .to_string(index=False)
        )

    # 11. Exportar el informe
    archivo_salida = "alojamientos_infravalorados.csv"

    infravalorados.to_csv(
        archivo_salida,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nInforme guardado como:", archivo_salida)

# =============================================================
# EJERCICIO 11B: MAPA INTERACTIVO DE OPORTUNIDADES EN GRECIA
# =============================================================

print("\n🗺️ Generando mapa de alojamientos infravalorados...")

import folium
from folium.plugins import MarkerCluster

# 1. Detectar las columnas de coordenadas disponibles
columnas_latitud = ["latitude", "lat", "Latitude", "Lat", "latitude_clean"]
columnas_longitud = ["longitude", "lon", "lng", "Longitude", "Lon", "longitude_clean"]

col_lat = next(
    (c for c in columnas_latitud if c in infravalorados.columns),
    None
)
col_lon = next(
    (c for c in columnas_longitud if c in infravalorados.columns),
    None
)

if col_lat is None or col_lon is None:
    print(
        "No se puede generar el mapa: no se encuentran las "
        "columnas de latitud y longitud."
    )
    print("Columnas disponibles:", infravalorados.columns.tolist())

else:
    # 2. Preparar los alojamientos con coordenadas válidas
    mapa_datos = infravalorados.copy()

    mapa_datos[col_lat] = pd.to_numeric(
        mapa_datos[col_lat], errors="coerce"
    )
    mapa_datos[col_lon] = pd.to_numeric(
        mapa_datos[col_lon], errors="coerce"
    )

    mapa_datos = mapa_datos.dropna(subset=[col_lat, col_lon])

    mapa_datos = mapa_datos[
        mapa_datos[col_lat].between(34, 42)
        & mapa_datos[col_lon].between(19, 30)
    ].copy()

    # 3. Mostrar las 1.000 mejores oportunidades por descuento
    mapa_datos = mapa_datos.sort_values(
        "descuento_pct", ascending=False
    ).head(1000)

    if mapa_datos.empty:
        print("No hay alojamientos con coordenadas válidas en Grecia.")

    else:
        # 4. Crear el mapa centrado en Grecia
        mapa_oportunidades = folium.Map(
            location=[39.0, 22.0],
            zoom_start=6,
            tiles="OpenStreetMap"
        )

        agrupador = MarkerCluster(
            name="Alojamientos infravalorados"
        ).add_to(mapa_oportunidades)

        # 5. Incorporar cada alojamiento al mapa
        for _, fila in mapa_datos.iterrows():

            precio = float(fila["price"])
            descuento = float(fila["descuento_pct"])
            mediana = float(fila["precio_mediano_comparable"])
            valoracion = fila.get("review_scores_rating", "No disponible")

            nombre = str(fila.get("name", "Sin nombre"))
            region = str(fila.get("region_origen", "Sin región"))
            tipo = str(fila.get("room_type", "No especificado"))
            capacidad = fila.get("accommodates", "No disponible")

            popup_html = f"""
            <div style="width:260px">
                <h4>{nombre}</h4>
                <b>Región:</b> {region}<br>
                <b>Tipo:</b> {tipo}<br>
                <b>Capacidad:</b> {capacidad} huéspedes<br>
                <b>Precio anunciado:</b> {precio:.2f} €<br>
                <b>Precio mediano comparable:</b> {mediana:.2f} €<br>
                <b>Descuento estimado:</b> {descuento:.1f}%<br>
                <b>Valoración:</b> {valoracion}<br>
                <b>ID:</b> {fila.get("id", "No disponible")}
            </div>
            """

            # Color según el descuento estimado
            if descuento >= 60:
                color = "green"
            elif descuento >= 40:
                color = "orange"
            else:
                color = "blue"

            folium.CircleMarker(
                location=[fila[col_lat], fila[col_lon]],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.75,
                tooltip=f"{nombre} | Descuento: {descuento:.1f}%",
                popup=folium.Popup(popup_html, max_width=320)
            ).add_to(agrupador)

        # 6. Añadir leyenda
        leyenda = """
        <div style="
            position: fixed;
            bottom: 30px; left: 30px; width: 240px;
            background: white; border: 2px solid #777;
            z-index: 9999; padding: 10px; font-size: 13px;">
            <b>Oportunidades de precio</b><br>
            <span style="color:green">●</span> Descuento ≥ 60%<br>
            <span style="color:orange">●</span> Descuento 40–59,9%<br>
            <span style="color:blue">●</span> Descuento 20–39,9%<br>
            <small>Se muestran hasta 1.000 alojamientos.</small>
        </div>
        """

        mapa_oportunidades.get_root().html.add_child(
            folium.Element(leyenda)
        )

        folium.LayerControl().add_to(mapa_oportunidades)

       
        # 7. Guardar el mapa junto al programa
        import os
        import socket
        import subprocess
        import sys
        import time
        import webbrowser

        carpeta_script = os.path.dirname(
            os.path.abspath(__file__)
        )

        archivo_mapa = "mapa_alojamientos_infravalorados.html"
        ruta_mapa = os.path.join(carpeta_script, archivo_mapa)

        mapa_oportunidades.save(ruta_mapa)

        print("Alojamientos incluidos en el mapa:", len(mapa_datos))
        print("Mapa guardado en:", ruta_mapa)

        # 8. Comprobar si el servidor del puerto 8000 está activo
        servidor_activo = False

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            servidor_activo = (
                s.connect_ex(("127.0.0.1", 8000)) == 0
            )

        # 9. Arrancar automáticamente el servidor si es necesario
        if not servidor_activo:
            print("Iniciando servidor web en el puerto 8000...")

            opciones = {
                "cwd": carpeta_script,
                "stdin": subprocess.DEVNULL,
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL
            }

            if os.name == "nt":
                opciones["creationflags"] = (
                    subprocess.CREATE_NO_WINDOW |
                    subprocess.CREATE_NEW_PROCESS_GROUP
                )

            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "http.server",
                    "8000",
                    "--bind",
                    "127.0.0.1"
                ],
                **opciones
            )

            # Esperar hasta que el servidor esté disponible
            for intento in range(20):
                time.sleep(0.5)

                with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                ) as s:
                    if s.connect_ex(("127.0.0.1", 8000)) == 0:
                        servidor_activo = True
                        break

        # 10. Abrir el mapa directamente en el navegador
        if servidor_activo:
            url_mapa = (
                "http://127.0.0.1:8000/"
                "mapa_alojamientos_infravalorados.html"
            )

            print("Abriendo el mapa en el navegador...")
            webbrowser.open(url_mapa)
            print("Dirección del mapa:", url_mapa)

        else:
            print("No se pudo iniciar el servidor web.")
            print("Comprueba si el puerto 8000 está disponible.")


# -------------------------------------------------------------
# 7. INICIAR SERVIDOR WEB Y ABRIR EL MAPA AUTOMÁTICAMENTE
# -------------------------------------------------------------

import subprocess
import sys
import os
import socket
import time
import webbrowser

CARPETA_DATOS = os.path.dirname(os.path.abspath(__file__))
PUERTO = 8000

# Comprobar si el servidor ya está activo
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    servidor_activo = s.connect_ex(("127.0.0.1", PUERTO)) == 0

# Iniciar el servidor si no está activo
if not servidor_activo:
    print("\nIniciando servidor web: py -m http.server 8000")

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(PUERTO),
            "--bind",
            "127.0.0.1"
        ],
        cwd=CARPETA_DATOS,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=(
            subprocess.CREATE_NO_WINDOW
            if os.name == "nt" else 0
        )
    )

    # Esperar a que el servidor esté disponible
    for _ in range(20):
        time.sleep(0.5)
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as s:
            if s.connect_ex(("127.0.0.1", PUERTO)) == 0:
                servidor_activo = True
                break

# Abrir el informe de rentabilidad si existe
archivo_resumen = os.path.join(
    CARPETA_DATOS,
    "resumen_rentabilidad_airbnb.csv"
)

if servidor_activo and os.path.exists(archivo_resumen):
    webbrowser.open(
        f"http://127.0.0.1:{PUERTO}/resumen_rentabilidad_airbnb.csv"
    )
    print("Informe de rentabilidad abierto en el navegador.")
else:
    print("Servidor no disponible o informe no encontrado.")

# -------------------------------------------------------------
# 8. DISEÑO Y CREACIÓN DE CUADRO DE MANDO EN FORMATO html.
# -------------------------------------------------------------

import pandas as pd
import json
from pathlib import Path

# ==========================================
# 1. CARGAR EL FICHERO CSV
# ==========================================

carpeta = Path(__file__).parent
archivo_csv = carpeta / "airbnb_grecia_clean(2).csv"

df = pd.read_csv(archivo_csv)

# Convertir columnas numéricas
columnas_numericas = [
    "price", "accommodates", "bedrooms", "beds",
    "number_of_reviews", "review_scores_rating",
    "latitude", "longitude", "bathrooms_num"
]

for columna in columnas_numericas:
    if columna in df.columns:
        df[columna] = pd.to_numeric(
            df[columna], errors="coerce"
        )

# Completar campos de texto vacíos
columnas_texto = [
    "name", "host_name", "neighbourhood_cleansed",
    "room_type", "region_origen",
    "host_is_superhost", "listing_url"
]

for columna in columnas_texto:
    if columna in df.columns:
        df[columna] = df[columna].fillna("")

# ==========================================
# 2. PREPARAR LOS DATOS PARA EL HTML
# ==========================================

datos = df.to_dict(orient="records")

# Convertir NaN y valores NumPy a JSON válido
datos_json = json.dumps(
    datos,
    ensure_ascii=False,
    allow_nan=False,
    default=lambda x: None
)

# ==========================================
# 3. CREAR EL CUADRO DE MANDO HTML
# ==========================================

html = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Cuadro de mando Airbnb Grecia</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #f2f5f9;
    color: #1c2b3a;
    margin: 0;
}
header {
    background: #1d527a;
    color: white;
    padding: 24px;
}
main {
    max-width: 1400px;
    margin: auto;
    padding: 20px;
}
.panel {
    background: white;
    padding: 18px;
    margin-bottom: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px #0000000d;
}
.filtros, .indicadores, .graficos {
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(190px,1fr));
    gap: 12px;
}
label {
    display: block;
    font-size: 12px;
    margin-bottom: 5px;
    color: #526477;
}
input, select, button {
    box-sizing: border-box;
    padding: 10px;
    width: 100%;
    border: 1px solid #ccd6e0;
    border-radius: 7px;
    background: white;
}
button {
    cursor: pointer;
    background: #1d527a;
    color: white;
}
.kpi {
    border-left: 4px solid #20a39e;
    padding: 12px;
    background: #f8fbfd;
}
.kpi strong {
    display: block;
    font-size: 25px;
    margin-top: 8px;
}
canvas {
    width: 100%;
    height: 260px;
}
.tabla {
    overflow: auto;
    max-height: 500px;
}
table {
    border-collapse: collapse;
    width: 100%;
    background: white;
    font-size: 12px;
}
th, td {
    padding: 9px;
    border-bottom: 1px solid #e1e7ed;
    text-align: left;
    white-space: nowrap;
}
th {
    background: #eaf0f6;
    position: sticky;
    top: 0;
}
a {
    color: #1d527a;
}
@media(max-width:650px) {
    main { padding: 10px; }
}
</style>
</head>

<body>

<header>
<h1>Cuadro de mando · Airbnb Grecia</h1>
<p>Análisis de precios, regiones, capacidad y valoraciones</p>
</header>

<main>

<section class="panel">
<h2>Filtros</h2>
<div class="filtros">
  <div>
    <label>Región</label>
    <select id="region">
      <option value="">Todas</option>
    </select>
  </div>
  <div>
    <label>Tipo de alojamiento</label>
    <select id="tipo">
      <option value="">Todos</option>
    </select>
  </div>
  <div>
    <label>Precio mínimo (€)</label>
    <input id="min" type="number" min="0">
  </div>
  <div>
    <label>Precio máximo (€)</label>
    <input id="max" type="number" min="0">
  </div>
  <div>
    <label>Capacidad mínima</label>
    <select id="capacidad">
      <option value="0">Cualquiera</option>
      <option value="2">2 personas</option>
      <option value="4">4 personas</option>
      <option value="6">6 personas</option>
      <option value="8">8 personas</option>
    </select>
  </div>
  <div>
    <label>Valoración mínima</label>
    <select id="valoracion">
      <option value="0">Cualquiera</option>
      <option value="4">4,0</option>
      <option value="4.5">4,5</option>
      <option value="4.8">4,8</option>
    </select>
  </div>
  <div>
    <label>Buscar alojamiento o barrio</label>
    <input id="buscar" type="search">
  </div>
  <div>
    <label>Ordenar por precio</label>
    <select id="orden">
      <option value="asc">Menor a mayor</option>
      <option value="desc">Mayor a menor</option>
    </select>
  </div>
  <div>
    <label>&nbsp;</label>
    <button onclick="reiniciar()">Restablecer filtros</button>
  </div>
</div>
</section>

<section class="indicadores">
  <div class="panel kpi">Alojamientos<strong id="total">—</strong></div>
  <div class="panel kpi">Precio medio<strong id="medio">—</strong></div>
  <div class="panel kpi">Precio mediano<strong id="mediana">—</strong></div>
  <div class="panel kpi">Valoración media<strong id="nota">—</strong></div>
  <div class="panel kpi">Capacidad media<strong id="personas">—</strong></div>
</section>

<section class="graficos">
  <div class="panel">
    <h2>Precio mediano por región</h2>
    <canvas id="graficoRegion"></canvas>
  </div>
  <div class="panel">
    <h2>Alojamientos por tipo</h2>
    <canvas id="graficoTipo"></canvas>
  </div>
</section>

<section class="panel">
<h2>Detalle de alojamientos</h2>
<p id="contador"></p>
<button onclick="descargarCSV()">Descargar resultados filtrados CSV</button>
<br><br>
<div class="tabla">
<table>
<thead>
<tr>
<th>Nombre</th>
<th>Región</th>
<th>Barrio</th>
<th>Tipo</th>
<th>Precio/noche</th>
<th>Capacidad</th>
<th>Valoración</th>
<th>Reseñas</th>
<th>Anuncio</th>
</tr>
</thead>
<tbody id="filas"></tbody>
</table>
</div>
<div style="display:flex;gap:10px;margin-top:12px">
<button onclick="paginaAnterior()">Anterior</button>
<span id="pagina" style="padding:10px"></span>
<button onclick="paginaSiguiente()">Siguiente</button>
</div>
</section>

</main>

<script>
const DATOS = __DATOS__;

const $ = id => document.getElementById(id);
let resultados = [];
let numeroPagina = 0;
const POR_PAGINA = 50;

function numero(v) {
    if (v === null || v === "" || v === undefined) return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
}

function euros(v) {
    if (v === null || !Number.isFinite(v)) return "—";
    return new Intl.NumberFormat("es-ES", {
        style: "currency",
        currency: "EUR",
        maximumFractionDigits: 2
    }).format(v);
}

function promedio(a) {
    return a.length ? a.reduce((s,v) => s+v,0)/a.length : null;
}

function mediana(a) {
    if (!a.length) return null;
    const b = [...a].sort((x,y) => x-y);
    const m = Math.floor(b.length/2);
    return b.length % 2 ? b[m] : (b[m-1]+b[m])/2;
}

function texto(v) {
    return String(v ?? "").replace(/[&<>"']/g, c => ({
        "&":"&amp;", "<":"&lt;", ">":"&gt;",
        '"':"&quot;", "'":"&#39;"
    })[c]);
}

function rellenarSelect(id, valores) {
    [...new Set(valores.filter(v => v !== "" && v != null))]
        .sort()
        .forEach(v => {
            const op = document.createElement("option");
            op.value = v;
            op.textContent = v;
            $(id).appendChild(op);
        });
}

rellenarSelect("region", DATOS.map(d => d.region_origen));
rellenarSelect("tipo", DATOS.map(d => d.room_type));

function filtrar() {
    const region = $("region").value;
    const tipo = $("tipo").value;
    const min = numero($("min").value);
    const max = numero($("max").value);
    const capacidad = Number($("capacidad").value);
    const valoracion = Number($("valoracion").value);
    const buscar = $("buscar").value.toLowerCase();

    resultados = DATOS.filter(d => {
        const p = numero(d.price);
        const c = numero(d.accommodates);
        const r = numero(d.review_scores_rating);

        if (region && d.region_origen !== region) return false;
        if (tipo && d.room_type !== tipo) return false;
        if (min !== null && (p === null || p < min)) return false;
        if (max !== null && (p === null || p > max)) return false;
        if (capacidad && (c === null || c < capacidad)) return false;
        if (valoracion && (r === null || r < valoracion)) return false;

        const textoBusqueda =
            `${d.name} ${d.neighbourhood_cleansed} ${d.host_name}`
            .toLowerCase();

        if (buscar && !textoBusqueda.includes(buscar)) return false;
        return true;
    });

    resultados.sort((a,b) => {
        const pa = numero(a.price) ?? Infinity;
        const pb = numero(b.price) ?? Infinity;
        return $("orden").value === "asc" ? pa-pb : pb-pa;
    });

    numeroPagina = 0;
    actualizar();
}

function actualizar() {
    const precios = resultados.map(d=>numero(d.price))
        .filter(v=>v!==null && v>=0);
    const notas = resultados.map(d=>numero(d.review_scores_rating))
        .filter(v=>v!==null);
    const capacidades = resultados.map(d=>numero(d.accommodates))
        .filter(v=>v!==null);

    $("total").textContent = resultados.length.toLocaleString("es-ES");
    $("medio").textContent = euros(promedio(precios));
    $("mediana").textContent = euros(mediana(precios));
    $("nota").textContent = promedio(notas)?.toFixed(2) ?? "—";
    $("personas").textContent = promedio(capacidades)?.toFixed(1) ?? "—";
    $("contador").textContent =
        `${resultados.length.toLocaleString("es-ES")} alojamientos encontrados`;

    dibujarRegion();
    dibujarTipo();
    dibujarTabla();
}

function prepararCanvas(id) {
    const canvas = $(id);
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = 260 * dpr;
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr,0,0,dpr,0,0);
    ctx.clearRect(0,0,rect.width,260);
    return {ctx,w:rect.width,h:260};
}

function dibujarRegion() {
    const {ctx,w,h} = prepararCanvas("graficoRegion");
    const regiones = [...new Set(resultados.map(d=>d.region_origen))];
    const valores = regiones.map(r=>mediana(resultados
        .filter(d=>d.region_origen===r)
        .map(d=>numero(d.price))
        .filter(v=>v!==null && v>=0)));

    const max = Math.max(...valores.filter(v=>v!==null),1);
    const ancho = (w-70)/Math.max(regiones.length,1);

    regiones.forEach((r,i)=>{
        const v = valores[i] ?? 0;
        const alto = v/max*(h-65);
        const x = 55+i*ancho;
        ctx.fillStyle="#2368a0";
        ctx.fillRect(x,h-40-alto,Math.max(10,ancho*.55),alto);
        ctx.fillStyle="#24364a";
        ctx.font="11px Arial";
        ctx.fillText(euros(v),x,h-45-alto);
        ctx.save();
        ctx.translate(x,h-22);
        ctx.rotate(-.25);
        ctx.fillText(r,0,0);
        ctx.restore();
    });
}

function dibujarTipo() {
    const {ctx,w,h} = prepararCanvas("graficoTipo");
    const tipos = [...new Set(resultados.map(d=>d.room_type))];
    const valores = tipos.map(t=>resultados.filter(d=>d.room_type===t).length);
    const max = Math.max(...valores,1);
    const ancho = (w-60)/Math.max(tipos.length,1);

    tipos.forEach((t,i)=>{
        const alto = valores[i]/max*(h-70);
        const x=40+i*ancho;
        ctx.fillStyle="#20a39e";
        ctx.fillRect(x,h-40-alto,Math.max(10,ancho*.55),alto);
        ctx.fillStyle="#24364a";
        ctx.font="11px Arial";
        ctx.fillText(valores[i],x,h-45-alto);
        ctx.save();
        ctx.translate(x,h-22);
        ctx.rotate(-.25);
        ctx.fillText(t.slice(0,22),0,0);
        ctx.restore();
    });
}

function dibujarTabla() {
    const inicio = numeroPagina*POR_PAGINA;
    const pagina = resultados.slice(inicio,inicio+POR_PAGINA);

    $("filas").innerHTML = pagina.map(d => `
      <tr>
        <td>${texto(d.name || "Sin nombre")}</td>
        <td>${texto(d.region_origen)}</td>
        <td>${texto(d.neighbourhood_cleansed)}</td>
        <td>${texto(d.room_type)}</td>
        <td>${euros(numero(d.price))}</td>
        <td>${numero(d.accommodates) ?? "—"}</td>
        <td>${numero(d.review_scores_rating) ?? "—"}</td>
        <td>${numero(d.number_of_reviews) ?? "—"}</td>
        <td>${d.listing_url
          ? `<a href="${texto(d.listing_url)}" target="_blank" rel="noopener">Ver anuncio</a>`
          : "—"}</td>
      </tr>`).join("");

    const paginas = Math.max(1,Math.ceil(resultados.length/POR_PAGINA));
    $("pagina").textContent = `Página ${numeroPagina+1} de ${paginas}`;
}

function paginaAnterior() {
    if (numeroPagina>0) {
        numeroPagina--;
        dibujarTabla();
    }
}

function paginaSiguiente() {
    if ((numeroPagina+1)*POR_PAGINA<resultados.length) {
        numeroPagina++;
        dibujarTabla();
    }
}

function reiniciar() {
    ["region","tipo","min","max","buscar"].forEach(id=>$(id).value="");
    $("capacidad").value="0";
    $("valoracion").value="0";
    $("orden").value="asc";
    filtrar();
}

function descargarCSV() {
    const cabecera = [
      "id","name","region_origen","neighbourhood_cleansed",
      "room_type","price","accommodates",
      "review_scores_rating","number_of_reviews","listing_url"
    ];

    const filas = resultados.map(d=>cabecera.map(k=>
        '"' + String(d[k] ?? "").replace(/"/g,'""') + '"'
    ).join(";"));

    const contenido = "\ufeff" + [
        cabecera.join(";"), ...filas
    ].join("\r\n");

    const blob = new Blob([contenido], {type:"text/csv;charset=utf-8"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href=url;
    a.download="airbnb_grecia_filtrado.csv";
    a.click();
    URL.revokeObjectURL(url);
}

["region","tipo","min","max","capacidad","valoracion","buscar","orden"]
.forEach(id => $(id).addEventListener("input",filtrar));

window.addEventListener("resize",actualizar);
filtrar();
</script>
</body>
</html>
"""

html = html.replace("__DATOS__", datos_json)

# ==========================================
# 4. GUARDAR EL ARCHIVO HTML
# ==========================================

archivo_html = carpeta / "cuadro_mando_airbnb_grecia.html"
archivo_html.write_text(html, encoding="utf-8")

print("Cuadro de mando creado correctamente.")
print("Registros:", len(df))
print("Archivo:", archivo_html)


























