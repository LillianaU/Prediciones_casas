# Tutorial del proyecto: Prediccion del valor medio de vivienda

## Estructura

```
Prediciones_casas/
  app.py          App web (Streamlit) — interfaz grafica
  predict.py      Script por consola (CLI) — predicciones por lotes
  .streamlit/
    secrets.toml  Credenciales de DataRobot
```

---

## app.py — Aplicacion web interactiva

**Que hace:** Muestra un formulario en el navegador para que ingreses datos de una vivienda y obtengas su valor estimado desde un modelo en DataRobot.

**Flujo:**
1. Carga las credenciales desde `.streamlit/secrets.toml`
2. Muestra formulario con 9 variables de la vivienda:
   - Coordenadas (longitud, latitud)
   - Edad mediana de la vivienda
   - Total de habitaciones y dormitorios
   - Poblacion y hogares
   - Ingreso mediano
   - Proximidad al oceano
3. Convierte los datos a CSV y los envia a la API de DataRobot
4. Muestra el resultado: valor estimado + graficos

**Graficos incluidos (Plotly):**
- **Radar:** perfil visual de las variables
- **Barras:** comparativa de valores
- **Gauge:** medidor con el precio estimado
- **Histograma:** distribucion de predicciones (modo batch)

**Modo Batch (2da pestana):**
- Subes un archivo CSV con muchas filas
- Se procesa con la API Batch Predictions de DataRobot (usa `predict.py` como modulo)
- Barra de progreso, resultados descargables

**Tecnologias:** Streamlit, Pandas, Requests, Plotly, importa `predict.py` como modulo.

---

## predict.py — Script de linea de comandos

**Que hace:** Procesa archivos CSV grandes mediante la API Batch Predictions de DataRobot, sin interfaz grafica.

**Uso tipico:**
```bash
python predict.py entrada.csv salida.csv <deployment_id> --api_key <key> --host <url>
```

**Parametros principales:**
| Parametro | Descripcion |
|-----------|-------------|
| `input-file.csv` | Archivo con datos a predecir |
| `output-file.csv` | Archivo donde se guardan los resultados |
| `deployment_id` | ID del modelo en DataRobot |
| `--host` | URL de DataRobot (default: https://app.datarobot.com) |
| `--api_key` | API key personal |
| `--n_concurrent` | Numero de peticiones simultaneas |

**Como funciona:**
1. Crea un trabajo batch en DataRobot via API
2. Sube el archivo CSV al servicio
3. Espera mientras el modelo procesa (con polling cada 15 segundos)
4. Descarga los resultados en el archivo de salida

**Usos:** ideal para lotes de datos, automatizaciones, CI/CD.

---

## app.py + predict.py — Como se relacionan

`app.py` importa `predict.py` como modulo para reutilizar sus funciones de conexion a la API Batch Predictions (no lo modifica, solo lo llama). Esto permite tener prediccion individual (API v2 directa) y por lotes (Batch Predictions) desde la misma interfaz web.

---

## Requisitos para ejecutar

1. Python 3.10+
2. Instalar dependencias: `pip install -r requirements.txt`
3. Archivo `.streamlit/secrets.toml` con:
   ```toml
   DATAROBOT_API_KEY = "tu_api_key"
   DATAROBOT_DEPLOYMENT_ID = "6a34f06404f39a876cdc194b"
   DATAROBOT_HOST = "https://app.datarobot.com"
   ```
4. Ejecutar: `streamlit run app.py`
