import streamlit as st
import pandas as pd

st.set_page_config(page_title="Alquila un Socio - MVP", layout="wide")

# Inicializar estados de los botones para que no rompa el hilo de renderizado
socios_data = [
    {"Nombre": "Carlos R.", "Habilidad": "Growth Marketing", "Industria": "Fintech / SaaS", "Disponibilidad": "10h/semana"},
    {"Nombre": "Ana M.", "Habilidad": "Desarrollo Fullstack", "Industria": "E-commerce", "Disponibilidad": "20h/semana"},
]
df_socios = pd.DataFrame(socios_data)

# Control de vistas básico
if "formulario_completado" not in st.session_state:
    st.session_state.formulario_completado = False

st.title("🤝 Alquila un Socio (MVP)")

if not st.session_state.formulario_completado:
    st.header("📋 Formulario de Madurez")
    with st.form("form_madurez"):
        p1 = st.text_area("1. ¿Cuál es el problema exacto y urgente?")
        enviar = st.form_submit_button("🚀 Evaluar")
        if enviar:
            st.session_state.formulario_completado = True
            st.rerun()
else:
    st.success("🎉 ¡Tu proyecto está listo!")
    st.header("🔎 Directorio")
    
    for idx, row in df_socios.iterrows():
        with st.container():
            col_info, col_accion = st.columns([3, 1])
            with col_info:
                st.subheader(row["Nombre"])
                st.write(f"🎯 **{row['Habilidad']}** | 🏢 {row['Industria']}")
            with col_accion:
                if st.button("🔒 Contactar", key=f"btn_{idx}"):
                    st.session_state[f"ver_pago_{idx}"] = True
            
            if st.session_state.get(f"ver_pago_{idx}", False):
                st.info(f"### 💳 Transferí $5.000 ARS al alias: **alquila.tu.socio.mp** y mandá el comprobante a soporte@alquilaundocio.com para desbloquear a {row['Nombre']}.")
            st.divider()
