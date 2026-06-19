# Requerimientos y ejecucion del proyecto

Este proyecto es una aplicacion de prediccion de valor de vivienda construida con Streamlit. La app principal esta en `app.py` y consulta un modelo desplegado en DataRobot usando credenciales configuradas como secretos locales.

## Requisitos del sistema

- Python 3.10 o superior.
- Acceso a internet para consultar la API de DataRobot.
- Credenciales validas de DataRobot:
  - `DATAROBOT_API_KEY`
  - `DATAROBOT_KEY`, si el deployment lo requiere
  - `DATAROBOT_DEPLOYMENT_ID`
  - `DATAROBOT_HOST`

## Dependencias de Python

Las dependencias estan definidas en `requirements.txt`:

```txt
streamlit>=1.35
pandas>=2.0
requests>=2.31
```

## Crear y activar el entorno virtual

Desde la raiz del proyecto:

```powershell
python -m venv .venv
```

Activar el entorno virtual en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion por politica de ejecucion, usar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

En Git Bash o Linux/macOS:

```bash
source .venv/bin/activate
```

## Instalar dependencias

Con el entorno virtual activado:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configurar secretos de DataRobot

Crear el archivo `.streamlit/secrets.toml` en la raiz del proyecto. Este archivo no debe subirse a Git.

Ejemplo:

```toml
DATAROBOT_API_KEY = "tu_api_key_real"
DATAROBOT_KEY = "tu_datarobot_key_si_el_deployment_lo_pide"
DATAROBOT_DEPLOYMENT_ID = "6a34f06404f39a876cdc194b"
DATAROBOT_HOST = "https://app.datarobot.com"
```

Si tu organizacion usa un dominio propio de DataRobot, cambia `DATAROBOT_HOST` por ese host, por ejemplo:

```toml
DATAROBOT_HOST = "https://tu-dominio.datarobot.com"
```

## Ejecutar la aplicacion

Con el entorno virtual activado:

```powershell
streamlit run app.py
```

Streamlit abrira la aplicacion en el navegador. Normalmente la URL local sera:

```text
http://localhost:8501
```

## Estructura principal

```text
app.py                  Aplicacion Streamlit interactiva.
requirements.txt        Dependencias del entorno virtual.
REQUERIMIENTOS.md       Guia de instalacion y ejecucion.
.streamlit/secrets.toml Credenciales locales, no versionadas.
```

## Problemas comunes

- `KeyError: DATAROBOT_API_KEY`: falta configurar `.streamlit/secrets.toml`.
- Error 401 o 403 desde DataRobot: la API key no es valida o no tiene permisos sobre el deployment.
- Error 404 desde DataRobot: el `DATAROBOT_DEPLOYMENT_ID` o el host no corresponden.
- `streamlit` no se reconoce como comando: el entorno virtual no esta activado o no se instalaron las dependencias.
