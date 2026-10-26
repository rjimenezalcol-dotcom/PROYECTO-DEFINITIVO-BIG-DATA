
# -*- coding: utf-8 -*-
"""
CUADRO DE MANDO AIRBNB GRECIA
Lee airbnb_grecia_clean.csv y genera cuadro_mando_airbnb.html
"""

from pathlib import Path
import json
import webbrowser
import pandas as pd
import numpy as np

# ==========================================================
# 1. CONFIGURACION DE ARCHIVOS
# ==========================================================

CARPETA = Path(__file__).resolve().parent

ARCHIVO_CSV = CARPETA / "airbnb_grecia_clean.csv"
ARCHIVO_HTML = CARPETA / "cuadro_mando_airbnb.html"

if not ARCHIVO_CSV.exists():
    print("ERROR: No se encuentra el archivo CSV.")
    print("Ruta buscada:", ARCHIVO_CSV)
    print("Archivos CSV disponibles:")
    for archivo in CARPETA.glob("*.csv"):
        print(" -", archivo.name)
    raise FileNotFoundError(
        "Guarda airbnb_grecia_clean.csv en la carpeta del script."
    )

# ==========================================================
# 2. LECTURA DEL CSV
# ==========================================================

df = None

for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
    try:
        df = pd.read_csv(
            ARCHIVO_CSV,
            encoding=encoding,
            sep=None,
            engine="python"
        )
        break
    except Exception:
        continue

if df is None:
    raise ValueError("No se ha podido leer el archivo CSV.")

if df.empty:
    raise ValueError("El archivo CSV no contiene registros.")

df.columns = [str(c).strip() for c in df.columns]

print("Archivo CSV:", ARCHIVO_CSV.name)
print("Registros:", len(df))
print("Columnas:", list(df.columns))

# ==========================================================
# 3. DETECCION AUTOMATICA DE COLUMNAS
# ==========================================================

def normalizar(texto):
    texto = str(texto).lower().strip()

    reemplazos = {
        "á": "a", "é": "e", "í": "i",
        "ó": "o", "ú": "u", "ñ": "n"
    }

    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)

    return texto.replace(" ", "_").replace("-", "_")


def buscar_columna(opciones):
    columnas_normalizadas = {
        normalizar(col): col for col in df.columns
    }

    for opcion in opciones:
        clave = normalizar(opcion)
        if clave in columnas_normalizadas:
            return columnas_normalizadas[clave]

    for opcion in opciones:
        clave = normalizar(opcion)

        for clave_columna, columna_original in columnas_normalizadas.items():
            if clave in clave_columna:
                return columna_original

    return None


col_precio = buscar_columna([
    "price", "precio", "precio_noche",
    "nightly_price", "price_per_night"
])

col_region = buscar_columna([
    "region_origen", "region", "zona",
    "ciudad", "city", "isla", "area",
    "neighbourhood_group", "neighborhood_group"
])

col_tipo = buscar_columna([
    "room_type", "tipo_habitacion",
    "tipo_alojamiento", "property_type"
])

col_nombre = buscar_columna([
    "name", "nombre", "listing_name", "title", "titulo"
])

col_rating = buscar_columna([
    "review_scores_rating", "rating",
    "calificacion", "puntuacion"
])

col_resenas = buscar_columna([
    "number_of_reviews", "num_reviews",
    "numero_resenas", "reviews"
])

# ==========================================================
# 4. LIMPIEZA DE DATOS NUMERICOS
# ==========================================================

def convertir_numero(serie):
    """
    Convierte precios y otros campos numéricos.
    Admite valores con coma decimal o punto decimal.
    """

    def convertir(valor):
        if pd.isna(valor):
            return np.nan

        texto = str(valor).strip()
        texto = texto.replace("€", "").replace("$", "")
        texto = texto.replace(" ", "")

        if texto.lower() in ("", "nan", "none", "null"):
            return np.nan

        if "," in texto and "." in texto:
            if texto.rfind(",") > texto.rfind("."):
                texto = texto.replace(".", "")
                texto = texto.replace(",", ".")
            else:
                texto = texto.replace(",", "")

        elif "," in texto:
            partes = texto.split(",")

            if len(partes[-1]) in (1, 2):
                texto = "".join(partes[:-1]) + "." + partes[-1]
            else:
                texto = "".join(partes)

        try:
            return float(texto)
        except ValueError:
            return np.nan

    return serie.map(convertir)


if col_precio:
    df["_precio"] = convertir_numero(df[col_precio])
else:
    df["_precio"] = np.nan

if col_rating:
    df["_rating"] = convertir_numero(df[col_rating])
else:
    df["_rating"] = np.nan

if col_resenas:
    df["_resenas"] = convertir_numero(df[col_resenas])
else:
    df["_resenas"] = np.nan

precios = df.loc[df["_precio"] > 0, "_precio"].dropna()
ratings = df["_rating"].dropna()

precio_medio = (
    float(precios.mean()) if not precios.empty else None
)

precio_mediano = (
    float(precios.median()) if not precios.empty else None
)

precio_minimo = (
    float(precios.min()) if not precios.empty else None
)

precio_maximo = (
    float(precios.max()) if not precios.empty else None
)

rating_medio = (
    float(ratings.mean()) if not ratings.empty else None
)

# ==========================================================
# 5. ANALISIS POR REGION
# ==========================================================

datos_region = []
datos_precio_region = []

if col_region:
    regiones = (
        df[col_region]
        .fillna("Sin especificar")
        .astype(str)
        .str.strip()
    )

    conteo = regiones.value_counts().head(15)

    datos_region = [
        {"label": str(nombre), "value": int(valor)}
        for nombre, valor in conteo.items()
    ]

    if col_precio:
        temporal = pd.DataFrame({
            "region": regiones,
            "precio": df["_precio"]
        })

        medias = (
            temporal[temporal["precio"] > 0]
            .groupby("region")["precio"]
            .mean()
            .sort_values()
            .head(15)
        )

        datos_precio_region = [
            {"label": str(nombre), "value": round(float(valor), 2)}
            for nombre, valor in medias.items()
        ]

# ==========================================================
# 6. ANALISIS POR TIPO DE ALOJAMIENTO
# ==========================================================

datos_tipo = []

if col_tipo:
    tipos = (
        df[col_tipo]
        .fillna("Sin especificar")
        .astype(str)
        .str.strip()
    )

    conteo_tipos = tipos.value_counts().head(12)

    datos_tipo = [
        {"label": str(nombre), "value": int(valor)}
        for nombre, valor in conteo_tipos.items()
    ]

# ==========================================================
# 7. DISTRIBUCION DE PRECIOS
# ==========================================================

datos_histograma = []

if not precios.empty:
    numero_intervalos = min(
        15,
        max(5, int(np.sqrt(len(precios))))
    )

    frecuencias, limites = np.histogram(
        precios,
        bins=numero_intervalos
    )

    for i, frecuencia in enumerate(frecuencias):
        datos_histograma.append({
            "label": (
                f"{limites[i]:.0f} - {limites[i + 1]:.0f}"
            ),
            "value": int(frecuencia)
        })

# ==========================================================
# 8. TOP 10 ALOJAMIENTOS MAS ECONOMICOS
# ==========================================================

top_alojamientos = []

if col_precio:
    top = (
        df[df["_precio"] > 0]
        .sort_values("_precio")
        .head(10)
    )

    for indice, fila in top.iterrows():

        nombre = (
            str(fila[col_nombre])
            if col_nombre and pd.notna(fila[col_nombre])
            else f"Alojamiento {indice}"
        )

        region = (
            str(fila[col_region])
            if col_region and pd.notna(fila[col_region])
            else "N/D"
        )

        tipo = (
            str(fila[col_tipo])
            if col_tipo and pd.notna(fila[col_tipo])
            else "N/D"
        )

        rating = fila["_rating"]

        top_alojamientos.append({
            "nombre": nombre,
            "region": region,
            "tipo": tipo,
            "precio": round(float(fila["_precio"]), 2),
            "rating": (
                None if pd.isna(rating)
                else round(float(rating), 2)
            )
        })

# ==========================================================
# 9. TABLA DE DATOS
# ==========================================================

columnas_originales = [
    col for col in df.columns
    if not col.startswith("_")
]

tabla_df = df[columnas_originales].head(100)

tabla = (
    tabla_df.astype(object)
    .where(pd.notna(tabla_df), None)
    .to_dict(orient="records")
)

# ==========================================================
# 10. PREPARAR DATOS PARA EL HTML
# ==========================================================

datos = {
    "archivo": ARCHIVO_CSV.name,
    "total": int(len(df)),
    "columnas": columnas_originales,
    "precioMedio": precio_medio,
    "precioMediano": precio_mediano,
    "precioMinimo": precio_minimo,
    "precioMaximo": precio_maximo,
    "ratingMedio": rating_medio,
    "datosRegion": datos_region,
    "datosPrecioRegion": datos_precio_region,
    "datosTipo": datos_tipo,
    "datosHistograma": datos_histograma,
    "top": top_alojamientos,
    "tabla": tabla
}

json_datos = json.dumps(
    datos,
    ensure_ascii=False,
    allow_nan=False,
    default=str
)

# ==========================================================
# 11. GENERAR EL CUADRO DE MANDO HTML
# ==========================================================

html = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cuadro de mando Airbnb Grecia</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {
    margin: 0;
    background: #f1f5f9;
    color: #1e293b;
    font-family: Arial, sans-serif;
}

header {
    background: #123b55;
    color: white;
    padding: 28px;
}

header h1 {
    margin-top: 0;
}

main {
    max-width: 1450px;
    margin: auto;
    padding: 22px;
}

.kpis {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
}

.card {
    background: white;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 3px 12px #0000000b;
    min-width: 0;
}

.kpi-label {
    color: #64748b;
    font-size: 14px;
}

.kpi-value {
    font-size: 27px;
    font-weight: bold;
    margin-top: 10px;
}

.charts {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
    margin-bottom: 20px;
}

.chart {
    height: 350px;
}

.chart canvas {
    max-height: 285px;
}

.table-wrap {
    overflow-x: auto;
    max-height: 480px;
}

table {
    border-collapse: collapse;
    width: 100%;
    background: white;
    font-size: 13px;
}

th, td {
    border-bottom: 1px solid #e2e8f0;
    padding: 10px;
    text-align: left;
}

th {
    background: #eaf0f6;
    position: sticky;
    top: 0;
}

input {
    padding: 10px;
    margin: 10px 0;
    width: min(350px, 90%);
}

button {
    padding: 10px 15px;
    background: #176b87;
    color: white;
    border: 0;
    border-radius: 6px;
    cursor: pointer;
}

.note {
    font-size: 12px;
    color: #64748b;
}

@media (max-width: 800px) {
    .charts {
        grid-template-columns: 1fr;
    }
}
</style>
</head>

<body>

<header>
    <h1>Cuadro de mando · Airbnb Grecia</h1>
    <p id="subtitulo"></p>
</header>

<main>

    <p id="archivo"></p>

    <section class="kpis" id="kpis"></section>

    <section class="charts">

        <article class="card chart">
            <h3>Alojamientos por región</h3>
            <canvas id="graficoRegion"></canvas>
            <p id="sinRegion" hidden>No se detectó la columna de región.</p>
        </article>

        <article class="card chart">
            <h3>Precio medio por región</h3>
            <canvas id="graficoPrecioRegion"></canvas>
            <p id="sinPrecioRegion" hidden>No hay datos suficientes.</p>
        </article>

        <article class="card chart">
            <h3>Distribución de precios</h3>
            <canvas id="graficoPrecios"></canvas>
            <p id="sinPrecios" hidden>No se detectaron precios válidos.</p>
        </article>

        <article class="card chart">
            <h3>Alojamientos por tipo</h3>
            <canvas id="graficoTipo"></canvas>
            <p id="sinTipo" hidden>No se detectó la columna de tipo.</p>
        </article>

    </section>

    <section class="card" style="margin-bottom:20px">
        <h2>Top 10 alojamientos más económicos</h2>

        <div class="table-wrap">
            <table id="tablaTop">
                <thead>
                    <tr>
                        <th>Posición</th>
                        <th>Alojamiento</th>
                        <th>Región</th>
                        <th>Tipo</th>
                        <th>Precio</th>
                        <th>Valoración</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>

        <p class="note">
            Ranking calculado a partir de los precios positivos del CSV.
            Comprueba la moneda y el periodo de los precios originales.
        </p>
    </section>

    <section class="card">
        <h2>Datos del CSV</h2>

        <input id="busqueda" placeholder="Buscar en la tabla...">

        <div class="table-wrap">
            <table id="tablaDatos">
                <thead></thead>
                <tbody></tbody>
            </table>
        </div>

        <p class="note">
            Se muestran las primeras 100 filas para facilitar la consulta.
        </p>
    </section>

    <p style="margin-top:20px">
        <button onclick="window.print()">Imprimir / Guardar como PDF</button>
    </p>

</main>

<script>
const D = __DATOS__;

function numero(v) {
    if (v === null || v === undefined || !Number.isFinite(Number(v))) {
        return "N/D";
    }
    return Number(v).toLocaleString("es-ES", {
        maximumFractionDigits: 2
    });
}

function escapar(valor) {
    return String(valor ?? "").replace(/[&<>"']/g, c => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }[c]));
}

document.getElementById("subtitulo").textContent =
    D.total.toLocaleString("es-ES") + " registros analizados";

document.getElementById("archivo").textContent =
    "Archivo: " + D.archivo +
    " | Columnas: " + D.columnas.length;

const indicadores = [
    ["Total de alojamientos", numero(D.total)],
    ["Precio medio", numero(D.precioMedio)],
    ["Precio mediano", numero(D.precioMediano)],
    ["Precio mínimo", numero(D.precioMinimo)],
    ["Precio máximo", numero(D.precioMaximo)],
    ["Valoración media", numero(D.ratingMedio)]
];

document.getElementById("kpis").innerHTML = indicadores.map(x =>
    `<article class="card">
        <div class="kpi-label">${x[0]}</div>
        <div class="kpi-value">${x[1]}</div>
    </article>`
).join("");

function crearGrafico(id, tipo, filas, etiqueta, horizontal=false) {
    if (!filas || filas.length === 0) {
        return false;
    }

    new Chart(document.getElementById(id), {
        type: tipo,
        data: {
            labels: filas.map(x => x.label),
            datasets: [{
                label: etiqueta,
                data: filas.map(x => x.value),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: horizontal ? "y" : "x",
            plugins: {
                legend: {
                    display: tipo === "doughnut"
                }
            },
            scales: tipo === "doughnut" ? {} : {
                y: { beginAtZero: true }
            }
        }
    });

    return true;
}

if (!crearGrafico("graficoRegion", "bar",
                  D.datosRegion, "Alojamientos", true)) {
    document.getElementById("sinRegion").hidden = false;
    document.getElementById("graficoRegion").hidden = true;
}

if (!crearGrafico("graficoPrecioRegion", "bar",
                  D.datosPrecioRegion, "Precio medio", true)) {
    document.getElementById("sinPrecioRegion").hidden = false;
    document.getElementById("graficoPrecioRegion").hidden = true;
}

if (!crearGrafico("graficoPrecios", "bar",
                  D.datosHistograma, "Alojamientos")) {
    document.getElementById("sinPrecios").hidden = false;
    document.getElementById("graficoPrecios").hidden = true;
}

if (!crearGrafico("graficoTipo", "doughnut",
                  D.datosTipo, "Alojamientos")) {
    document.getElementById("sinTipo").hidden = false;
    document.getElementById("graficoTipo").hidden = true;
}

// Tabla del Top 10
const cuerpoTop = document.querySelector("#tablaTop tbody");

cuerpoTop.innerHTML = D.top.map((fila, i) => `
    <tr>
        <td>${i + 1}</td>
        <td>${escapar(fila.nombre)}</td>
        <td>${escapar(fila.region)}</td>
        <td>${escapar(fila.tipo)}</td>
        <td>${numero(fila.precio)}</td>
        <td>${numero(fila.rating)}</td>
    </tr>
`).join("");

// Tabla general
const cabecera = document.querySelector("#tablaDatos thead");
const cuerpo = document.querySelector("#tablaDatos tbody");

cabecera.innerHTML = "<tr>" + D.columnas.map(col =>
    `<th>${escapar(col)}</th>`
).join("") + "</tr>";

function pintarTabla(filtro = "") {
    const q = filtro.toLowerCase();

    const filas = D.tabla.filter(fila =>
        D.columnas.some(col =>
            String(fila[col] ?? "").toLowerCase().includes(q)
        )
    );

    cuerpo.innerHTML = filas.map(fila =>
        "<tr>" + D.columnas.map(col =>
            `<td>${escapar(fila[col])}</td>`
        ).join("") + "</tr>"
    ).join("");
}

pintarTabla();

document.getElementById("busqueda").addEventListener("input", e => {
    pintarTabla(e.target.value);
});
</script>

</body>
</html>
"""

html = html.replace("__DATOS__", json_datos)

# ==========================================================
# 12. GUARDAR Y ABRIR EL HTML
# ==========================================================

ARCHIVO_HTML.write_text(html, encoding="utf-8")

print("\n" + "=" * 55)
print("CUADRO DE MANDO GENERADO CORRECTAMENTE")
print("=" * 55)
print("Archivo CSV:", ARCHIVO_CSV)
print("Registros:", len(df))
print("Columna de precio:", col_precio or "No detectada")
print("Columna de región:", col_region or "No detectada")
print("Columna de tipo:", col_tipo or "No detectada")
print("Archivo HTML:", ARCHIVO_HTML)
print("=" * 55)

webbrowser.open(ARCHIVO_HTML.resolve().as_uri())
