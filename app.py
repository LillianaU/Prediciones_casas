import pandas as pd
import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


st.set_page_config(
    page_title="Prediccion valor vivienda",
    page_icon="house",
    layout="wide",
)

st.markdown(
    """
    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >
    <style>
        .stApp {
            background: #f5f7fb;
        }

        .main .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero {
            background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 48%, #20c997 100%);
            border-radius: 18px;
            color: white;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 18px 45px rgba(13, 110, 253, 0.22);
        }

        .hero h1 {
            font-size: clamp(2rem, 4vw, 3.2rem);
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .hero p {
            font-size: 1.05rem;
            margin-bottom: 0;
            opacity: 0.92;
        }

        .section-title {
            color: #1f2937;
            font-weight: 750;
            margin-top: 0.4rem;
            margin-bottom: 0.8rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 14px;
            border-color: rgba(15, 23, 42, 0.08);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }

        .stButton > button {
            background: #0d6efd;
            border: 1px solid #0d6efd;
            border-radius: 10px;
            color: white;
            font-weight: 700;
            min-height: 3rem;
            width: 100%;
        }

        .stButton > button:hover {
            background: #0b5ed7;
            border-color: #0b5ed7;
            color: white;
        }

        .config-card {
            background: #fff3cd;
            border: 1px solid #ffecb5;
            border-radius: 12px;
            color: #664d03;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
        }

        .success-card {
            background: #d1e7dd;
            border: 1px solid #badbcc;
            border-radius: 12px;
            color: #0f5132;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <span class="badge text-bg-light mb-3">DataRobot - Regresion</span>
        <h1>Prediccion del valor medio de vivienda</h1>
        <p>Modifica las variables de entrada y consulta el modelo desplegado en DataRobot.</p>
    </section>
    """,
    unsafe_allow_html=True,
)


def load_datarobot_config():
    try:
        api_key = st.secrets["DATAROBOT_API_KEY"]
        deployment_id = st.secrets["DATAROBOT_DEPLOYMENT_ID"]
        host = st.secrets["DATAROBOT_HOST"].rstrip("/")
        datarobot_key = st.secrets.get("DATAROBOT_KEY", "").strip()
        return api_key, deployment_id, host, datarobot_key
    except (KeyError, StreamlitSecretNotFoundError):
        st.markdown(
            """
            <div class="config-card">
                <h5 class="mb-2">Falta configurar DataRobot</h5>
                <p class="mb-0">
                    Crea el archivo <strong>.streamlit/secrets.toml</strong> y agrega
                    tu API key, el ID del deployment y el host de DataRobot.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.code(
            '''DATAROBOT_API_KEY = "tu_api_key_real"
DATAROBOT_KEY = "tu_datarobot_key_si_el_deployment_lo_pide"
DATAROBOT_DEPLOYMENT_ID = "6a34f06404f39a876cdc194b"
DATAROBOT_HOST = "https://app.datarobot.com"''',
            language="toml",
        )
        st.info(
            "La app necesita ese archivo local para leer tus credenciales privadas. "
            "No lo subas a GitHub."
        )
        st.stop()


(
    DATAROBOT_API_KEY,
    DATAROBOT_DEPLOYMENT_ID,
    DATAROBOT_HOST,
    DATAROBOT_KEY,
) = load_datarobot_config()

PREDICTION_URL = (
    f"{DATAROBOT_HOST}/predApi/v1.0/deployments/"
    f"{DATAROBOT_DEPLOYMENT_ID}/predictions"
)

HEADERS = {
    "Authorization": f"Bearer {DATAROBOT_API_KEY}",
    "Content-Type": "text/plain; charset=UTF-8",
}

if DATAROBOT_KEY:
    HEADERS["DataRobot-Key"] = DATAROBOT_KEY

left_col, right_col = st.columns([1.05, 0.95], gap="large")

with left_col:
    with st.container(border=True):
        st.markdown('<h3 class="section-title">Variables de entrada</h3>', unsafe_allow_html=True)

        geo_col_1, geo_col_2 = st.columns(2)
        with geo_col_1:
            longitud = st.number_input("Longitud", value=-122.23, step=0.01)
        with geo_col_2:
            latitud = st.number_input("Latitud", value=37.88, step=0.01)

        edad_mediana_vivienda = st.slider(
            "Edad mediana de la vivienda",
            min_value=1,
            max_value=60,
            value=30,
        )

        housing_col_1, housing_col_2 = st.columns(2)
        with housing_col_1:
            total_habitaciones = st.number_input(
                "Total de habitaciones",
                min_value=1,
                value=880,
            )
        with housing_col_2:
            total_dormitorios = st.number_input(
                "Total de dormitorios",
                min_value=1,
                value=129,
            )

        people_col_1, people_col_2 = st.columns(2)
        with people_col_1:
            poblacion = st.number_input(
                "Poblacion",
                min_value=1,
                value=322,
            )
        with people_col_2:
            hogares = st.number_input(
                "Hogares",
                min_value=1,
                value=126,
            )

        ingreso_mediano = st.number_input(
            "Ingreso mediano",
            min_value=0.0,
            value=8.3252,
            step=0.01,
        )

        proximidad_oceano = st.selectbox(
            "Proximidad al oceano",
            [
                "NEAR BAY",
                "<1H OCEAN",
                "INLAND",
                "NEAR OCEAN",
                "ISLAND",
            ],
        )

datos = pd.DataFrame(
    [
        {
            "longitud": longitud,
            "latitud": latitud,
            "edad_mediana_vivienda": edad_mediana_vivienda,
            "total_habitaciones": total_habitaciones,
            "total_dormitorios": total_dormitorios,
            "poblacion": poblacion,
            "hogares": hogares,
            "ingreso_mediano": ingreso_mediano,
            "proximidad_oceano": proximidad_oceano,
        }
    ]
)

csv_data = datos.to_csv(index=False)

with right_col:
    with st.container(border=True):
        st.markdown('<h3 class="section-title">Datos enviados</h3>', unsafe_allow_html=True)
        st.dataframe(datos, use_container_width=True, hide_index=True)

    with st.container(border=True):
        st.markdown('<h3 class="section-title">Resultado</h3>', unsafe_allow_html=True)

        if st.button("Predecir valor de vivienda"):
            try:
                response = requests.post(
                    PREDICTION_URL,
                    headers=HEADERS,
                    data=csv_data.encode("utf-8"),
                    timeout=60,
                )

                if response.status_code == 200:
                    resultado = response.json()
                    prediccion = resultado["data"][0]["prediction"]

                    st.markdown(
                        """
                        <div class="success-card">
                            <strong>Prediccion realizada correctamente.</strong>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.metric(
                        label="Valor medio estimado de la vivienda",
                        value=f"${prediccion:,.2f}",
                    )

                    with st.expander("Ver respuesta completa de DataRobot"):
                        st.json(resultado)

                else:
                    st.error("Error al consultar DataRobot")
                    st.write("Codigo:", response.status_code)
                    if response.status_code == 403:
                        st.warning(
                            "DataRobot rechazo la solicitud por permisos. Revisa que la API key "
                            "tenga acceso al deployment y, si el deployment lo requiere, agrega "
                            "DATAROBOT_KEY en .streamlit/secrets.toml."
                        )
                    st.write(response.text)

            except requests.RequestException as exc:
                st.error("No fue posible conectar con DataRobot.")
                st.write(exc)
            except (KeyError, IndexError, TypeError) as exc:
                st.error("DataRobot respondio con un formato inesperado.")
                st.write(exc)
