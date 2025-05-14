import streamlit as st
import pandas as pd
import sys
import os

# Asegura que podamos importar la función desde el backend
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from compare import comparar_crf_vs_ehr

st.title("Comparador de datos clínicos: CRF vs Historia Clínica")

st.markdown("Sube dos archivos CSV para comparar datos del ensayo clínico.")

uploaded_crf = st.file_uploader("📄 Subir archivo CRF (cuaderno de recogida de datos)", type="csv")
uploaded_ehr = st.file_uploader("🩺 Subir archivo de datos fuente (EHR)", type="csv")

if uploaded_crf and uploaded_ehr:
    crf_df = pd.read_csv(uploaded_crf)
    ehr_df = pd.read_csv(uploaded_ehr)

    # Guardar temporalmente para pasar la ruta a la función
    crf_df.to_csv("crf_temp.csv", index=False)
    ehr_df.to_csv("ehr_temp.csv", index=False)

    st.success("Archivos cargados. Comparando datos...")

    resultado = comparar_crf_vs_ehr("crf_temp.csv", "ehr_temp.csv")

    if isinstance(resultado, str):
        st.warning(resultado)
    elif resultado:
        st.subheader("⚠️ Discrepancias encontradas:")
        resultado_df = pd.DataFrame(resultado)
        st.dataframe(resultado_df)
        st.download_button("Descargar reporte en CSV", resultado_df.to_csv(index=False), file_name="discrepancias.csv")
    else:
        st.success("✅ No se encontraron discrepancias.")