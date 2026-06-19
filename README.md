# Prediccion del valor medio de vivienda

Aplicacion web desarrollada con **Streamlit** para consultar un modelo de regresion desplegado en **DataRobot**. El usuario modifica variables de entrada de una vivienda y la aplicacion envia esos datos al deployment para obtener una prediccion del valor medio estimado.

## Vista general

```text
Usuario
  |
  v
App Streamlit
  |
  v
CSV con variables de vivienda
  |
  v
API de prediccion de DataRobot
  |
  v
Resultado de regresion: valor_mediano_vivienda
```

## Modelo

| Campo | Valor |
| --- | --- |
| Plataforma | DataRobot |
| Tipo de modelo | Regresion |
| Objetivo | valor_mediano_vivienda |
| Deployment ID | 6a34f06404f39a876cdc194b |
| Host | https://app.datarobot.com |

## Variables usadas por la aplicacion

La aplicacion envia un registro con estas variables:

| Variable | Descripcion |
| --- | --- |
| longitud | Coordenada geografica de longitud |
| latitud | Coordenada geografica de latitud |
| edad_mediana_vivienda | Edad mediana de las viviendas |
| total_habitaciones | Total de habitaciones |
| total_dormitorios | Total de dormitorios |
| poblacion | Poblacion del area |
| hogares | Numero de hogares |
| ingreso_mediano | Ingreso mediano |
| proximidad_oceano | Categoria de cercania al oceano |

Valores disponibles para `proximidad_oceano`:

```text
NEAR BAY
<1H OCEAN
INLAND
NEAR OCEAN
ISLAND
```

## Interfaz

La pantalla principal muestra:

- Un encabezado visual: **DataRobot - Regresion**.
- Un formulario con las variables de entrada.
- Una tabla con los datos enviados al modelo.
- Un boton para ejecutar la prediccion.
- Una tarjeta de resultado con el valor estimado.
- Un panel opcional para ver la respuesta completa de DataRobot.

Si falta la configuracion de DataRobot, la aplicacion muestra un aviso como este:

```text
Falta configurar DataRobot
Crea el archivo .streamlit/secrets.toml y agrega tu API key,
el ID del deployment y el host de DataRobot.
```

## Requisitos

- Python 3.10 o superior.
- Cuenta o acceso a DataRobot.
- Deployment activo en DataRobot.
- API key personal de DataRobot.
- Acceso a internet para consultar la API.

Dependencias principales:

```text
streamlit
pandas
requests
```

## Instalacion

Desde la carpeta raiz del proyecto:

```powershell
python -m venv .venv
```

Activar el entorno virtual en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuracion de DataRobot

La aplicacion necesita un archivo real llamado:

```text
.streamlit/secrets.toml
```

Crea o edita `.streamlit/secrets.toml` y reemplaza `tu_api_key_real` por tu clave real de DataRobot:

```toml
DATAROBOT_API_KEY = "tu_api_key_real"
DATAROBOT_KEY = "tu_datarobot_key_si_el_deployment_lo_pide"
DATAROBOT_DEPLOYMENT_ID = "6a34f06404f39a876cdc194b"
DATAROBOT_HOST = "https://app.datarobot.com"
```

### Donde obtener cada dato

| Variable | Donde se obtiene |
| --- | --- |
| DATAROBOT_API_KEY | Perfil de usuario en DataRobot, seccion de API Keys o Developer Tools |
| DATAROBOT_KEY | Snippet o ejemplo de consumo de la Prediction API del deployment, si DataRobot lo muestra |
| DATAROBOT_DEPLOYMENT_ID | Pagina del deployment del modelo en DataRobot |
| DATAROBOT_HOST | URL base donde entras a DataRobot |

Importante: no publiques el archivo `.streamlit/secrets.toml` en GitHub. Ese archivo contiene credenciales privadas.

## Ejecucion

Ejecutar la aplicacion:

```powershell
streamlit run app.py
```

Si el puerto predeterminado esta ocupado:

```powershell
streamlit run app.py --server.port 8502
```

Luego abre en el navegador:

```text
http://localhost:8501
```

o, si usaste el puerto 8502:

```text
http://localhost:8502
```

## Estructura del proyecto

```text
Prediciones_casas/
|
|-- app.py                         App principal en Streamlit
|-- requirements.txt               Dependencias de Python
|-- REQUERIMIENTOS.md              Guia de entorno virtual y ejecucion
|-- README.md                      Documentacion principal
|-- .gitignore                     Archivos excluidos de Git
|-- .streamlit/
|   |-- secrets.toml               Credenciales reales, no versionar
```

## Flujo tecnico de prediccion

1. El usuario completa los campos en la interfaz.
2. Streamlit crea un `DataFrame` con pandas.
3. El `DataFrame` se convierte a CSV.
4. La app envia el CSV a DataRobot con `requests.post`.
5. DataRobot responde con la prediccion.
6. Streamlit muestra el valor estimado en pantalla.

Endpoint construido por la aplicacion:

```text
https://app.datarobot.com/predApi/v1.0/deployments/6a34f06404f39a876cdc194b/predictions
```

## Problemas comunes

| Error | Causa probable | Solucion |
| --- | --- | --- |
| `StreamlitSecretNotFoundError` | No existe `.streamlit/secrets.toml` | Crear `.streamlit/secrets.toml` con las credenciales de DataRobot |
| Error 401 | API key invalida | Crear una nueva API key y actualizar `.streamlit/secrets.toml` |
| Error 403 | API key sin permisos o falta `DATAROBOT_KEY` | Revisar permisos del deployment y copiar `DATAROBOT_KEY` desde el snippet de Prediction API |
| Error 404 | Deployment ID o host incorrecto | Verificar el deployment activo en DataRobot |
| `streamlit` no se reconoce | Dependencias no instaladas o entorno inactivo | Activar `.venv` e instalar `requirements.txt` |
| No conecta con DataRobot | Sin internet, host incorrecto o bloqueo de red | Revisar conexion y URL del host |

## Seguridad

- No subir `.streamlit/secrets.toml` al repositorio.
- Si una API key fue compartida por error, revocarla y crear una nueva.
- Mantener las credenciales solo en `.streamlit/secrets.toml`.

## Comando rapido

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
