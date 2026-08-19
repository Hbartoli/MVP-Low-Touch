import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection  # Conector nativo seguro

# 1. Configuración de página
st.set_page_config(page_title="Alquila un Socio - MVP Low-Touch", layout="wide")

# 2. Inicialización del Estado de la Aplicación
if "formulario_completado" not in st.session_state:
    st.session_state.formulario_completado = False
if "nivel_madurez" not in st.session_state:
    st.session_state.nivel_madurez = None
if "puntos_madurez" not in st.session_state:
    st.session_state.puntos_madurez = 0

# 3. CONEXIÓN EN TIEMPO REAL A GOOGLE SHEETS
# Lee automáticamente el secreto configurado bajo el formato [connections]
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # ttl="10m" significa que cachea los datos por 10 minutos para ahorrar consumo, pero puedes bajarlo
    df_socios = conn.read(ttl="1m") 
except Exception as e:
    st.error("Error al conectar con la base de datos de socios. Verifica la configuración de Secrets.")
    df_socios = pd.DataFrame(columns=["Nombre", "Habilidad", "Industria", "Disponibilidad"])

# Título Principal
st.title("🤝 Alquila un Socio")
st.subheader("Plataforma de Matchmaking Autónomo para Startups")
st.divider()

# --- VISTA 1: FORMULARIO DE DIAGNÓSTICO INTERACTIVO ---
if not st.session_state.formulario_completado:
    st.header("📋 Formulario de Auto-Diagnóstico de Madurez")
    st.write("Completa este cuestionario para habilitar el acceso al directorio de socios.")

    with st.form("form_madurez"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🟢 Nivel 1: Problema y Cliente")
            p1 = st.text_area("1. ¿Cuál es el problema exacto que estás resolviendo?")
            p2 = st.text_area("2. ¿Quién es tu cliente ideal específico?")
            p3 = st.radio("3. ¿Conoces las alternativas actuales de tus clientes?", 
                          ["No las conozco", "Sí, usan planillas de Excel o procesos manuales deficientes"])
        with col2:
            st.markdown("### 🟡 Nivel 2: Validación y Rol")
            p4 = st.number_input("4. ¿Con cuántos clientes potenciales has hablado directamente?", min_value=0, step=1, value=0)
            p5 = st.radio("5. ¿Tienes alguna evidencia de interés comercial medible hoy?", 
                          ["Es solo una idea / No tengo registros", "Tengo lista de espera o cartas de intención de compra"])
            p6 = st.text_input("6. ¿Qué habilidad específica buscas en un socio?")

        enviar = st.form_submit_button("🚀 Evaluar Madurez de mi Startup")

        if enviar:
            puntos = 0
            if len(p1) > 25: puntos += 1
            if len(p2) > 15: puntos += 1
            if p3 == "Sí, usan planillas de Excel o procesos manuales deficientes": puntos += 1
            if p4 >= 10: puntos += 1
            if p5 == "Tengo lista de espera o cartas de intención de compra": puntos += 1
            if len(p6) > 10: puntos += 1

            st.session_state.puntos_madurez = puntos
            if puntos <= 3:
                st.session_state.nivel_madurez = "🔴 Etapa de Idea Básica (No Apto)"
            elif 4 <= puntos <= 5:
                st.session_state.nivel_madurez = "🟡 Etapa de Validación Media"
            else:
                st.session_state.nivel_madurez = "🟢 Listo para Matchmaking"
                
            st.session_state.formulario_completado = True
            st.rerun()

# --- VISTA 2: RESULTADOS Y ACCESO FILTRADO ---
else:
    st.header(f"Resultado de tu Evaluación: {st.session_state.nivel_madurez}")
    
    if st.session_state.nivel_madurez == "🔴 Etapa de Idea Básica (No Apto)":
        st.error("❌ Tu proyecto se encuentra en una etapa muy temprana.")
        st.info("💡 **Siguiente paso:** Realiza al menos 10 entrevistas reales antes de volver a intentar.")
        if st.button("🔄 Reiniciar Formulario"):
            st.session_state.formulario_completado = False
            st.rerun()
    else:
        st.success("🎉 ¡Tu proyecto cumple con los requisitos mínimos!")
        
        # --- DIRECTORIO DE SOCIOS DESDE GOOGLE SHEETS ---
        st.header("🔎 Directorio de Socios Disponibles")
        
        if not df_socios.empty:
            categorias_disponibles = list(df_socios["Habilidad"].dropna().unique())
            filtro_habilidad = st.selectbox("Filtrar por Especialidad del Socio:", categorias_disponibles)
            socios_filtrados = df_socios[df_socios["Habilidad"] == filtro_habilidad]
            
            for idx, row in socios_filtrados.iterrows():
                with st.container():
                    col_info, col_accion = st.columns(3,1)
                    with col_info:
                        st.subheader(row["Nombre"])
                        st.write(f"🎯 **Especialidad:** {row['Habilidad']} | 🏢 **Industria:** {row['Industria']} | ⏱️ **Disponibilidad:** {row['Disponibilidad']}")
                    with col_accion:
                        if st.button("🔒 Solicitar Contacto", key=f"btn_{idx}", use_container_width=True):
                            st.session_state[f"ver_pago_{idx}"] = True

                    if st.session_state.get(f"ver_pago_{idx}", False):
                        st.warning("### 💳 Instrucciones para Desbloquear Contacto")
                        st.write("Abona una tarifa de validación única de **$5.000 ARS (o $5 USD)** para liberar canales directos.")
                        
                        pago_col1, pago_col2 = st.columns(2)
                        with pago_col1:
                            st.markdown("**Opción A:** Transferencia alias: `alquila.tu.socio.mp` (Mercado Pago)")
                        with pago_col2:
                            st.markdown("**Opción B:** PayPal cuenta: `pagos@alquilaundocio.com` ($5 USD)")
                        
                        st.markdown(f"📩 Envía tu comprobante a **soporte@alquilaundocio.com** indicando que deseas conectar con **{row['Nombre']}**.")
                        
                        if st.button("Ocultar Datos de Pago", key=f"hide_{idx}"):
                            st.session_state[f"ver_pago_{idx}"] = False
                            st.rerun()
                    st.divider()
        else:
            st.warning("No hay socios registrados en la base de datos actualmente.")
                
        if st.button("⬅️ Volver al Inicio"):
            st.session_state.formulario_completado = False
            st.rerun()

                
        if st.button("⬅️ Re-evaluar otro proyecto / Volver"):
            st.session_state.formulario_completado = False
            st.rerun()

