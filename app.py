import streamlit as st
import pandas as pd

# 1. Configuración de página y estilos básicos
st.set_page_config(
    page_title="Alquila un Socio - MVP Low-Touch", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Inicialización del Estado de la Aplicación (Evita reinicios de datos)
if "formulario_completado" not in st.session_state:
    st.session_state.formulario_completado = False
if "nivel_madurez" not in st.session_state:
    st.session_state.nivel_madurez = None
if "puntos_madurez" not in st.session_state:
    st.session_state.puntos_madurez = 0

# Base de datos simulada de Socios para el Directorio
socios_data = [
    {"Nombre": "Carlos R.", "Habilidad": "Growth Marketing", "Industria": "Fintech / SaaS", "Disponibilidad": "10h/semana"},
    {"Nombre": "Ana M.", "Habilidad": "Desarrollo Fullstack", "Industria": "E-commerce", "Disponibilidad": "20h/semana"},
    {"Nombre": "Diego F.", "Habilidad": "Diseño de Producto / UX", "Industria": "Salud / EdTech", "Disponibilidad": "15h/semana"}
]
df_socios = pd.DataFrame(socios_data)

# Título Principal Dinámico (Visual Anchor)
st.title("🤝 Alquila un Socio")
st.subheader("Plataforma de Matchmaking Autónomo para Startups")
st.divider()

# --- VISTA 1: FORMULARIO DE DIAGNÓSTICO INTERACTIVO ---
if not st.session_state.formulario_completado:
    st.header("📋 Formulario de Auto-Diagnóstico de Madurez")
    st.write("Completa este cuestionario para habilitar el acceso al directorio de socios. Evaluamos la tracción inicial de tu idea.")

    with st.form("form_madurez"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🟢 Nivel 1: Problema y Cliente")
            p1 = st.text_area(
                "1. ¿Cuál es el problema exacto y urgente que estás resolviendo?", 
                placeholder="Ej: Los directores de RRHH pierden 10h semanales filtrando CVs manualmente..."
            )
            p2 = st.text_area(
                "2. ¿Quién es tu cliente ideal específico?", 
                placeholder="Ej: Empresas SaaS de 10 a 50 empleados en Latam."
            )
            p3 = st.radio(
                "3. ¿Conoces las alternativas actuales con las que hoy resuelven este problema?", 
                ["No, asumo que no tienen competencia", "Sí, usan planillas de Excel o procesos manuales deficientes"]
            )

        with col2:
            st.markdown("### 🟡 Nivel 2: Validación y Rol")
            p4 = st.number_input(
                "4. ¿Con cuántos clientes potenciales has hablado directamente (entrevistas de problema)?", 
                min_value=0, step=1, value=0
            )
            p5 = st.radio(
                "5. ¿Tienes alguna evidencia de interés comercial medible hoy?", 
                ["Es solo una idea / No tengo registros", "Tengo lista de espera (+50 personas) o cartas de intención de compra"]
            )
            p6 = st.text_input(
                "6. ¿Qué habilidad específica buscas en un socio?", 
                placeholder="Ej: Desarrollador Fullstack con experiencia en IA"
            )

        # Botón de Procesamiento Automático
        enviar = st.form_submit_button("🚀 Evaluar Madurez de mi Startup")

        if enviar:
            # Algoritmo de Puntuación Automatizado (Filtro Low-Touch)
            puntos = 0
            if len(p1) > 25: puntos += 1
            if len(p2) > 15: puntos += 1
            if p3 == "Sí, usan planillas de Excel o procesos manuales deficientes": puntos += 1
            if p4 >= 10: puntos += 1
            if p5 == "Tengo lista de espera (+50 personas) o cartas de intención de compra": puntos += 1
            if len(p6) > 10: puntos += 1

            # Clasificación de Niveles de Madurez
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
    st.write(f"Puntuación obtenida: **{st.session_state.puntos_madurez} de 6 puntos posibles.**")
    
    # FLUJO BLOQUEADO: Usuario no apto (Ahorra tiempo de soporte técnico)
    if st.session_state.nivel_madurez == "🔴 Etapa de Idea Básica (No Apto)":
        st.error("❌ Tu proyecto se encuentra en una etapa muy temprana para conectar con socios de alto valor.")
        st.info(
            "💡 **Siguiente paso recomendado:** Para desbloquear el acceso al directorio, necesitas realizar "
            "al menos 10 entrevistas reales a tus clientes ideales y documentar sus alternativas actuales. "
            "Trabaja en la validación y vuelve a intentarlo."
        )
        if st.button("🔄 Reiniciar Formulario de Diagnóstico"):
            st.session_state.formulario_completado = False
            st.rerun()

    # FLUJO PERMITIDO: El proyecto tiene bases sólidas
    else:
        st.success("🎉 ¡Tu proyecto cumple con los requisitos mínimos de madurez del ecosistema!")
        st.balloons()
        
        # --- DIRECTORIO DE SOCIOS AUTOGESTIONADO ---
        st.header("🔎 Directorio de Socios Disponibles")
        st.write("Filtra y selecciona el perfil que mejor se adapte a las necesidades técnicas o comerciales de tu negocio.")
        
        # Filtros reactivos nativos de Streamlit
        categorias_disponibles = list(df_socios["Habilidad"].unique())
        filtro_habilidad = st.selectbox("Filtrar por Especialidad del Socio:", categorias_disponibles)
        socios_filtrados = df_socios[df_socios["Habilidad"] == filtro_habilidad]
        
        # Despliegue de tarjetas de socios
        for idx, row in socios_filtrados.iterrows():
            with st.container():
                col_info, col_accion = st.columns([3, 1])
                with col_info:
                    st.subheader(row["Nombre"])
                    st.write(f"🎯 **Especialidad:** {row['Habilidad']} | 🏢 **Industria:** {row['Industria']} | ⏱️ **Disponibilidad:** {row['Disponibilidad']}")
                with col_accion:
                    # Switch de estado para controlar la visualización de la pasarela por cada socio
                    if st.button("🔒 Solicitar Contacto", key=f"btn_{idx}", use_container_width=True):
                        st.session_state[f"ver_pago_{idx}"] = True

                # --- INTERFAZ DE MONETIZACIÓN FRICCIONAL (PAGO MANUAL) ---
                if st.session_state.get(f"ver_pago_{idx}", False):
                    st.warning(f"### 💳 Instrucciones Manuales para Desbloquear Contacto")
                    st.write(
                        "Para mantener la red libre de spam y asegurar perfiles comerciales comprometidos, "
                        "aplicamos una **tarifa de validación única de $5.000 ARS (o $5 USD)** para liberar canales directos."
                    )
                    
                    pago_col1, pago_col2 = st.columns(2)
                    with pago_col1:
                        st.markdown("""
                        **Opción A: Transferencia (Argentina)**
                        * **Alias:** alquila.tu.socio.mp
                        * **Banco:** Mercado Pago
                        * **Monto:** $5.000 ARS
                        """)
                    with pago_col2:
                        st.markdown("""
                        **Opción B: PayPal o Crypto (Internacional)**
                        * **Cuenta/Wallet:** pagos@alquilaundocio.com
                        * **Monto:** $5 USD
                        """)
                    
                    st.markdown(
                        f"📩 **Paso Final:** Envía tu comprobante de operación a **soporte@alquilaundocio.com** o vía WhatsApp. "
                        f"Indica tu correo de registro y el nombre del socio seleccionado (**{row['Nombre']}**). "
                        "Validaremos los fondos y recibirás su enlace de agenda/LinkedIn en menos de 2 horas."
                    )
                    
                    if st.button("Ocultar Datos de Pago", key=f"hide_{idx}"):
                        st.session_state[f"ver_pago_{idx}"] = False
                        st.rerun()
                st.divider()
                
        if st.button("⬅️ Re-evaluar otro proyecto / Volver"):
            st.session_state.formulario_completado = False
            st.rerun()
