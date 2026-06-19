import os
import tempfile
import threading
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

import predict


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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

        * { font-family: 'Inter', sans-serif; }

        .stApp {
            background: linear-gradient(135deg, #f0f4ff 0%, #e8ecf4 100%);
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .hero {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 20px;
            color: white;
            padding: 2.5rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 20px 60px rgba(15, 52, 96, 0.3);
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: rgba(255,255,255,0.03);
        }

        .hero::after {
            content: '';
            position: absolute;
            bottom: -30%;
            left: -10%;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: rgba(255,255,255,0.02);
        }

        .hero .badge {
            background: rgba(255,255,255,0.15) !important;
            color: #e0e7ff !important;
            font-weight: 600;
            padding: 0.35rem 1rem;
            border-radius: 50px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .hero h1 {
            font-size: clamp(2rem, 4vw, 3.2rem);
            font-weight: 900;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
            position: relative;
            z-index: 1;
        }

        .hero p {
            font-size: 1.05rem;
            margin-bottom: 0;
            opacity: 0.85;
            position: relative;
            z-index: 1;
        }

        .card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid rgba(0,0,0,0.04);
            margin-bottom: 1rem;
        }

        .card-title {
            color: #1a1a2e;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .card-title .icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }

        .icon-blue { background: #e8f0fe; color: #1a73e8; }
        .icon-green { background: #e6f4ea; color: #137333; }
        .icon-purple { background: #f3e8ff; color: #7c3aed; }
        .icon-orange { background: #fef3e8; color: #ea580c; }

        .stButton > button {
            background: linear-gradient(135deg, #1a73e8, #0f3460);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 700;
            min-height: 3.2rem;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
            letter-spacing: 0.3px;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(26, 115, 232, 0.4);
            color: white;
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: none !important;
            box-shadow: none !important;
        }

        .stSlider label, .stNumberInput label, .stSelectbox label {
            font-weight: 600 !important;
            color: #1a1a2e !important;
            font-size: 0.9rem !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: white;
            padding: 0.25rem;
            border-radius: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1.5rem;
            color: #64748b;
            border: none;
            transition: all 0.2s;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #1a73e8, #0f3460) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
        }

        .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            background: #f1f5f9;
            color: #1a1a2e;
        }

        .metric-card {
            background: linear-gradient(135deg, #1a73e8, #0f3460);
            border-radius: 16px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            box-shadow: 0 8px 30px rgba(26, 115, 232, 0.25);
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -30%;
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: rgba(255,255,255,0.05);
        }

        .metric-card .label {
            font-size: 0.9rem;
            font-weight: 500;
            opacity: 0.9;
            margin-bottom: 0.3rem;
        }

        .metric-card .value {
            font-size: 2.5rem;
            font-weight: 900;
            letter-spacing: -1px;
        }

        .metric-card .sub {
            font-size: 0.8rem;
            opacity: 0.7;
            margin-top: 0.25rem;
        }

        .success-msg {
            background: linear-gradient(135deg, #e6f4ea, #c8e6c9);
            border: 1px solid #a5d6a7;
            border-radius: 12px;
            color: #1b5e20;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
            font-weight: 500;
        }

        .config-card {
            background: #fff8e1;
            border: 1px solid #ffecb3;
            border-radius: 12px;
            color: #795548;
            padding: 1.25rem;
            margin: 1rem 0;
        }

        .batch-header {
            background: linear-gradient(135deg, #7c3aed, #1a73e8);
            border-radius: 16px;
            color: white;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 30px rgba(124, 58, 237, 0.25);
        }

        .upload-zone {
            border: 2px dashed #cbd5e1;
            border-radius: 16px;
            padding: 2.5rem 2rem;
            text-align: center;
            background: white;
            transition: all 0.3s;
        }

        .upload-zone:hover {
            border-color: #1a73e8;
            background: #f8faff;
        }

        .stDataFrame {
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }

        .stProgress > div > div {
            background: linear-gradient(90deg, #1a73e8, #7c3aed) !important;
            border-radius: 10px !important;
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }

            .hero {
                padding: 1.5rem 1.25rem;
                border-radius: 14px;
            }

            .hero::before, .hero::after {
                display: none;
            }

            .hero h1 {
                font-size: clamp(1.4rem, 5vw, 2rem);
            }

            .hero p {
                font-size: 0.9rem;
            }

            .hero .badge {
                font-size: 0.75rem;
                padding: 0.2rem 0.75rem;
            }

            .card {
                padding: 1rem;
                border-radius: 12px;
            }

            .card-title {
                font-size: 0.95rem;
            }

            .card-title .icon {
                width: 26px;
                height: 26px;
                font-size: 0.85rem;
            }

            .metric-card {
                padding: 1rem;
            }

            .metric-card .value {
                font-size: 1.6rem;
            }

            .metric-card .label {
                font-size: 0.8rem;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 0.4rem 0.8rem;
                font-size: 0.8rem;
            }

            .stTabs [data-baseweb="tab-list"] {
                padding: 0.15rem;
            }

            .upload-zone {
                padding: 1.5rem 1rem;
            }

            .upload-zone div[style*="font-size:3rem"] {
                font-size: 2rem !important;
            }

            .batch-header {
                padding: 1rem;
            }

            .batch-header h4 {
                font-size: 1rem;
            }

            .batch-header p {
                font-size: 0.85rem;
            }

            .stSlider label, .stNumberInput label, .stSelectbox label {
                font-size: 0.8rem !important;
            }
        }

        @media (min-width: 769px) and (max-width: 1024px) {
            .main .block-container {
                max-width: 960px;
                padding-top: 1.25rem;
            }

            .hero {
                padding: 2rem 1.5rem;
            }

            .hero h1 {
                font-size: clamp(1.6rem, 3.5vw, 2.4rem);
            }

            .card {
                padding: 1.25rem;
            }

            .metric-card .value {
                font-size: 2rem;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 0.5rem 1rem;
                font-size: 0.85rem;
            }
        }

        @media (max-width: 480px) {
            .hero {
                padding: 1rem 0.9rem;
                margin-bottom: 1rem;
            }

            .hero h1 {
                font-size: clamp(1.1rem, 5vw, 1.4rem);
            }

            .hero p {
                font-size: 0.8rem;
            }

            .card {
                padding: 0.75rem;
                margin-bottom: 0.75rem;
            }

            .card-title {
                font-size: 0.85rem;
                margin-bottom: 0.75rem;
            }

            .metric-card .value {
                font-size: 1.3rem;
            }

            .stButton > button {
                min-height: 2.6rem;
                font-size: 0.85rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <span class="badge mb-3">DataRobot &bull; Regresion</span>
        <h1>Prediccion del valor medio de vivienda</h1>
        <p>Ajusta las variables de entrada y consulta el modelo de regresion
        desplegado en DataRobot para estimar el valor de una vivienda.</p>
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

predict.api_host = DATAROBOT_HOST
predict.api_key = DATAROBOT_API_KEY

PREDICTION_URL = (
    f"{DATAROBOT_HOST}/api/v2/deployments/"
    f"{DATAROBOT_DEPLOYMENT_ID}/predictions"
)

HEADERS = {
    "Authorization": f"Token {DATAROBOT_API_KEY}",
    "Content-Type": "text/plain; charset=UTF-8",
}

if DATAROBOT_KEY:
    HEADERS["DataRobot-Key"] = DATAROBOT_KEY


def build_batch_payload():
    return {"deploymentId": DATAROBOT_DEPLOYMENT_ID}


def run_batch_prediction(input_path, output_path, payload, progress_bar, status_text):
    try:
        job = predict._request(
            "POST",
            predict.BATCH_PREDICTIONS_URL.format(host=DATAROBOT_HOST),
            data=payload,
        )
        job_url = job["links"]["self"]

        upload_thread = threading.Thread(
            target=predict.upload_datarobot_batch_predictions,
            args=(job, open(input_path, "rb")),
        )
        upload_thread.start()

        while True:
            time.sleep(predict.POLL_INTERVAL)
            job = predict._request("GET", job_url)
            job_status = job["status"]

            if job_status == predict.JobStatus.INITIALIZING:
                status_text.text("Inicializando trabajo...")
            elif job_status == predict.JobStatus.RUNNING:
                pct = float(job.get("percentageCompleted", 0)) / 100
                progress_bar.progress(pct)
                status_text.text(
                    f"Procesando: {pct:.1%} completado | "
                    f"{job.get('scoredRows', 0)} filas OK | "
                    f"{job.get('failedRows', 0)} errores"
                )
            elif job_status in (
                predict.JobStatus.COMPLETED,
                predict.JobStatus.ABORTED,
                predict.JobStatus.FAILED,
            ):
                upload_thread.join()
                progress_bar.progress(1.0)

                if job_status == predict.JobStatus.COMPLETED:
                    status_text.text("Descargando resultados...")
                    predict.download_datarobot_batch_predictions(job, open(output_path, "wb"))
                    return True, None
                else:
                    msg = job.get("statusDetails", "Sin detalles disponibles")
                    return False, msg

    except predict.DataRobotPredictionError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error inesperado: {e}"


def plot_input_radar(row):
    categories = [
        "Longitud", "Latitud", "Edad vivienda",
        "Habitaciones", "Dormitorios", "Poblacion",
        "Hogares", "Ingreso mediano",
    ]
    values = [
        row["longitud"], row["latitud"], row["edad_mediana_vivienda"],
        row["total_habitaciones"], row["total_dormitorios"],
        row["poblacion"], row["hogares"], row["ingreso_mediano"],
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[abs(v) if v else 0 for v in values],
        theta=categories,
        fill="toself",
        name="Valores",
        line=dict(color="#1a73e8", width=3),
        fillcolor="rgba(26, 115, 232, 0.15)",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, showticklabels=False), bgcolor="rgba(0,0,0,0)"),
        showlegend=False,
        margin=dict(l=40, r=40, t=10, b=10),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11, color="#334155"),
    )
    return fig


def plot_feature_bars(row):
    features = {
        "Edad vivienda": row["edad_mediana_vivienda"],
        "Total habitaciones": row["total_habitaciones"],
        "Dormitorios": row["total_dormitorios"],
        "Poblacion": row["poblacion"],
        "Hogares": row["hogares"],
        "Ingreso mediano": row["ingreso_mediano"],
    }
    df_features = pd.DataFrame(list(features.items()), columns=["Variable", "Valor"])
    colors = ["#1a73e8", "#4285f4", "#7c3aed", "#ea580c", "#059669", "#d97706"]

    fig = px.bar(
        df_features, x="Variable", y="Valor", text="Valor",
        color="Variable", color_discrete_sequence=colors,
    )
    fig.update_traces(
        textposition="outside", textfont=dict(size=12, weight=700, color="#1e293b"),
        marker_line=dict(width=0),
        hovertemplate="<b>%{x}</b><br>Valor: %{y}<extra></extra>",
    )
    fig.update_layout(
        xaxis=dict(title=None, tickfont=dict(size=11, weight=600, color="#475569"), gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(title=None, tickfont=dict(size=10, color="#94a3b8"), gridcolor="rgba(0,0,0,0.04)"),
        showlegend=False, margin=dict(l=10, r=10, t=10, b=60),
        height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def plot_prediction_gauge(prediction):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        number=dict(font=dict(size=40, weight=900, color="#1a1a2e"), prefix="$", valueformat=",.2f"),
        gauge=dict(
            axis=dict(range=[0, max(500000, prediction * 1.5)],
                      tickfont=dict(size=11, color="#64748b")),
            bar=dict(color="#1a73e8", thickness=0.4),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
            steps=[
                dict(range=[0, 150000], color="rgba(26, 115, 232, 0.06)"),
                dict(range=[150000, 300000], color="rgba(26, 115, 232, 0.10)"),
                dict(range=[300000, 500000], color="rgba(26, 115, 232, 0.14)"),
            ],
            threshold=dict(line=dict(color="#7c3aed", width=4), thickness=0.75, value=prediction),
        ),
    ))
    fig.update_layout(
        height=220, margin=dict(l=30, r=30, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"),
    )
    return fig


tab1, tab2 = st.tabs(["Prediccion individual", "Prediccion por lotes (Batch)"])


with tab1:
    left_col, mid_col, right_col = st.columns([1.2, 0.9, 1.2], gap="large")

    with left_col:
        st.markdown(
            '<div class="card"><div class="card-title">'
            '<span class="icon icon-blue">&#9881;</span> Variables de entrada</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            geo_col_1, geo_col_2 = st.columns(2)
            with geo_col_1:
                longitud = st.number_input("Longitud", value=-122.23, step=0.01, format="%.4f")
            with geo_col_2:
                latitud = st.number_input("Latitud", value=37.88, step=0.01, format="%.4f")

            edad_mediana_vivienda = st.slider("Edad mediana de la vivienda", 1, 60, 30)

            housing_col_1, housing_col_2 = st.columns(2)
            with housing_col_1:
                total_habitaciones = st.number_input("Total de habitaciones", 1, value=880)
            with housing_col_2:
                total_dormitorios = st.number_input("Total de dormitorios", 1, value=129)

            people_col_1, people_col_2 = st.columns(2)
            with people_col_1:
                poblacion = st.number_input("Poblacion", 1, value=322)
            with people_col_2:
                hogares = st.number_input("Hogares", 1, value=126)

            ingreso_mediano = st.number_input("Ingreso mediano", 0.0, value=8.3252, step=0.01, format="%.4f")

            proximidad_oceano = st.selectbox(
                "Proximidad al oceano",
                ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"],
            )

        st.markdown("</div>", unsafe_allow_html=True)

    datos = pd.DataFrame([{
        "longitud": longitud, "latitud": latitud,
        "edad_mediana_vivienda": edad_mediana_vivienda,
        "total_habitaciones": total_habitaciones, "total_dormitorios": total_dormitorios,
        "poblacion": poblacion, "hogares": hogares,
        "ingreso_mediano": ingreso_mediano, "proximidad_oceano": proximidad_oceano,
    }])

    csv_data = datos.to_csv(index=False)

    with mid_col:
        st.markdown(
            '<div class="card"><div class="card-title">'
            '<span class="icon icon-purple">&#9673;</span> Perfil de la vivienda</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(plot_input_radar(datos.iloc[0]), use_container_width=True, key="radar")
        st.markdown(
            '<div style="text-align:center;padding:0.25rem 0 0.75rem 0;font-size:0.8rem;color:#64748b;">'
            'Perfil de valores normalizados</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="card"><div class="card-title">'
            '<span class="icon icon-orange">&#9632;</span> Comparativa de variables</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(plot_feature_bars(datos.iloc[0]), use_container_width=True, key="bars")
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown(
            '<div class="card"><div class="card-title">'
            '<span class="icon icon-green">&#10003;</span> Datos enviados</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(datos, use_container_width=True, hide_index=True)
        st.caption(f"Proximidad: {proximidad_oceano} | Coordenadas: {latitud:.4f}, {longitud:.4f}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="card"><div class="card-title">'
            '<span class="icon icon-blue">&#9650;</span> Resultado</div>',
            unsafe_allow_html=True,
        )

        if st.button("Predecir valor de vivienda", key="predict_single", use_container_width=True):
            with st.spinner("Consultando modelo en DataRobot..."):
                try:
                    response = requests.post(
                        PREDICTION_URL, headers=HEADERS,
                        data=csv_data.encode("utf-8"), timeout=60,
                    )

                    if response.status_code == 200:
                        resultado = response.json()
                        prediccion = resultado["data"][0]["prediction"]

                        st.markdown(
                            '<div class="success-msg">Prediccion realizada correctamente</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<div class="metric-card">'
                            f'<div class="label">Valor medio estimado de la vivienda</div>'
                            f'<div class="value">${prediccion:,.2f}</div>'
                            f'<div class="sub">Basado en los valores ingresados</div></div>',
                            unsafe_allow_html=True,
                        )
                        st.plotly_chart(
                            plot_prediction_gauge(prediccion),
                            use_container_width=True, key="gauge",
                        )

                        with st.expander("Respuesta completa de DataRobot"):
                            st.json(resultado)
                    else:
                        st.error("Error al consultar DataRobot")
                        st.write("Codigo:", response.status_code)
                        st.write(response.text)

                except requests.RequestException as exc:
                    st.error("No fue posible conectar con DataRobot.")
                    st.write(exc)
                except (KeyError, IndexError, TypeError) as exc:
                    st.error("DataRobot respondio con un formato inesperado.")
                    st.write(exc)
        else:
            st.info("Ajusta las variables y presiona el boton para obtener una prediccion.")

        st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    st.markdown(
        '<div class="batch-header"><h4 class="mb-1">Prediccion por lotes</h4>'
        '<p class="mb-0">Sube un archivo CSV con multiples registros y procesalos en lote '
        'mediante la API Batch Predictions de DataRobot.</p></div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([1, 1], gap="large")

    with col_a:
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV", type="csv", key="batch_upload",
            help="Archivo CSV con las mismas columnas del formulario individual",
        )

        if uploaded_file is not None:
            st.markdown("---")
            try:
                uploaded_file.seek(0)
                df_preview = pd.read_csv(uploaded_file)
            except Exception:
                st.error("No se pudo leer el archivo CSV. Verifica el formato.")
                st.stop()

            st.markdown('<h5 style="font-weight:700;color:#1a1a2e;margin-bottom:0.75rem;">Vista previa</h5>',
                        unsafe_allow_html=True)
            st.dataframe(df_preview, use_container_width=True)

            f1, f2, f3, f4 = st.columns(4)
            f1.metric("Filas", len(df_preview))
            f2.metric("Columnas", len(df_preview.columns))
            f3.metric("Valores nulos", df_preview.isna().sum().sum())
            f4.metric("Columnas numericas", len(df_preview.select_dtypes(include="number").columns))

            uploaded_file.seek(0)

    with col_b:
        if uploaded_file is not None:
            st.markdown('<h5 style="font-weight:700;color:#1a1a2e;margin-bottom:1rem;">&nbsp;</h5>',
                        unsafe_allow_html=True)

            if st.button("Ejecutar prediccion por lotes", type="primary", use_container_width=True):
                tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
                try:
                    tmp_in.write(uploaded_file.getvalue())
                    tmp_in_path = tmp_in.name
                finally:
                    tmp_in.close()

                tmp_out_path = tempfile.mktemp(suffix=".csv")
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.text("Iniciando trabajo batch...")

                success, error_msg = run_batch_prediction(
                    tmp_in_path, tmp_out_path, build_batch_payload(), progress_bar, status_text,
                )

                try:
                    if success:
                        result_df = pd.read_csv(tmp_out_path)
                        st.markdown(
                            '<div class="success-msg">Prediccion por lotes completada exitosamente</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            '<h5 style="font-weight:700;color:#1a1a2e;margin:0.75rem 0;">Resultados</h5>',
                            unsafe_allow_html=True,
                        )
                        st.dataframe(result_df, use_container_width=True)

                        csv_result = result_df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "Descargar resultados (CSV)", csv_result,
                            "predicciones_resultado.csv", "text/csv",
                            use_container_width=True,
                        )

                        if "prediction" in result_df.columns:
                            st.markdown(
                                '<h6 style="font-weight:700;color:#1a1a2e;margin:1rem 0 0.5rem 0;">'
                                'Distribucion de predicciones</h6>',
                                unsafe_allow_html=True,
                            )
                            fig_hist = px.histogram(
                                result_df, x="prediction", nbins=30,
                                color_discrete_sequence=["#1a73e8"],
                                labels={"prediction": "Valor estimado", "count": "Frecuencia"},
                            )
                            fig_hist.update_traces(
                                marker_line=dict(width=1, color="white"),
                                hovertemplate="Valor: $%{x:,.2f}<br>Frecuencia: %{y}<extra></extra>",
                            )
                            fig_hist.update_layout(
                                margin=dict(l=10, r=10, t=10, b=40), height=250,
                                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                xaxis=dict(tickfont=dict(size=11, color="#475569"),
                                           gridcolor="rgba(0,0,0,0.04)", tickprefix="$"),
                                yaxis=dict(tickfont=dict(size=10, color="#94a3b8"),
                                           gridcolor="rgba(0,0,0,0.04)"),
                            )
                            st.plotly_chart(fig_hist, use_container_width=True, key="hist")

                        with st.expander("Estadisticas del resultado"):
                            numeric_cols = result_df.select_dtypes(include="number").columns
                            if len(numeric_cols) > 0:
                                st.dataframe(result_df[numeric_cols].describe(), use_container_width=True)
                    else:
                        st.error(f"Error en la prediccion por lotes: {error_msg}")

                except Exception as e:
                    st.error(f"Error al leer los resultados: {e}")
                finally:
                    os.unlink(tmp_in_path)
                    if os.path.exists(tmp_out_path):
                        os.unlink(tmp_out_path)
        else:
            st.markdown(
                '<div class="upload-zone">'
                '<div style="font-size:3rem;margin-bottom:0.75rem;color:#94a3b8;">&#128196;</div>'
                '<p style="font-size:1.1rem;color:#475569;font-weight:600;margin-bottom:0.5rem;">'
                'Arrastra un archivo CSV aqui</p>'
                '<p style="font-size:0.9rem;color:#94a3b8;margin-bottom:0;">'
                'o haz clic en "Browse files" para seleccionarlo</p></div>',
                unsafe_allow_html=True,
            )

            with st.expander("Formato esperado del CSV"):
                st.markdown(
                    "El archivo CSV debe incluir las siguientes columnas:\n\n"
                    "| Columna | Tipo | Ejemplo |\n"
                    "|---|---|---|\n"
                    "| longitud | float | -122.23 |\n"
                    "| latitud | float | 37.88 |\n"
                    "| edad_mediana_vivienda | int | 30 |\n"
                    "| total_habitaciones | int | 880 |\n"
                    "| total_dormitorios | int | 129 |\n"
                    "| poblacion | int | 322 |\n"
                    "| hogares | int | 126 |\n"
                    "| ingreso_mediano | float | 8.3252 |\n"
                    "| proximidad_oceano | string | NEAR BAY |\n\n"
                    "**Valores para `proximidad_oceano`:** NEAR BAY, <1H OCEAN, INLAND, NEAR OCEAN, ISLAND"
                )

                sample_df = pd.DataFrame([{
                    "longitud": -122.23, "latitud": 37.88, "edad_mediana_vivienda": 30,
                    "total_habitaciones": 880, "total_dormitorios": 129, "poblacion": 322,
                    "hogares": 126, "ingreso_mediano": 8.3252, "proximidad_oceano": "NEAR BAY",
                }])
                st.download_button(
                    "Descargar CSV de ejemplo",
                    sample_df.to_csv(index=False).encode("utf-8"),
                    "ejemplo_prediccion.csv", "text/csv",
                )
