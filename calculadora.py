import streamlit as st
from datetime import date

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Calculadora CTS 2026 Perú",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/JhovinB',
        'About': "# Calculadora de CTS Profesional\nDesarrollada para trabajadores de Perú siguiendo la Ley N.º 32322."
    }
)

# VERIFICACIÓN
st.markdown("""
    <head>
        <meta name="google-site-verification" content="6FhXLrOzwlJiAnoYcnU4Wn_NMv-y71-PH9lwi6WsYMk" />
    </head>
""", unsafe_allow_html=True)

# DISEÑO 
st.markdown("""
    <style>
    /* 1. ESTILOS DE MARCA Y CONTENEDORES */
    .stApp { background-color: #0f172a; }
    h1, h2, h3, p, label { color: #f8fafc !important; }
    
    div[data-testid="stVerticalBlock"] > div.stColumn > div {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #334155;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        font-weight: bold;
        border: none;
    }
    
    .result-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #38bdf8;
        text-align: center;
    }

    /* 2. LIMPIEZA TOTAL DE ELEMENTOS DE STREAMLIT (ELIMINA AVATAR Y CORONA) */
    
    /* Oculta la barra superior, el menú de hamburguesa y el pie de página */
    header, footer, #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }

    /* Elimina el widget de estado (Avatar y Corona en la esquina inferior derecha) */
    div[data-testid="stStatusWidget"], 
    .stStatusWidget,
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }

    /* Elimina cualquier botón de Deploy o sugerencia de edición */
    .stAppDeployButton, .stDeployButton, .stDecoration {
        display: none !important;
    }

    /* 3. OPTIMIZACIÓN DE ESPACIO */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ENCABEZADO
st.markdown(f"<h1 style='text-align: center;'>Calculadora CTS 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Simulación precisa según Ley N.º 32322 (Retiro 100%)</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

# LÓGICA
## Definimos las fechas
CORTE_MAYO = date(2026, 4, 30)
INICIO_MAYO = date(2025, 11, 1)

CORTE_NOVIEMBRE = date(2026, 10, 31)
INICIO_NOVIEMBRE = date(2026, 5, 1)

# INTERFAZ
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Ingreso de Datos")
    with st.container(border=True):
     
        fecha_ingreso = st.date_input("Fecha de Ingreso Laboral", value=date(2026, 1, 1))
       
        if fecha_ingreso <= CORTE_MAYO:
            nombre_periodo = "Mayo 2026"
            f_corte = CORTE_MAYO
            f_inicio = INICIO_MAYO
        else:
            nombre_periodo = "Noviembre 2026"
            f_corte = CORTE_NOVIEMBRE
            f_inicio = INICIO_NOVIEMBRE
        
        sueldo = st.number_input("Sueldo Bruto Mensual (S/.)", value=0.0, step=100.0)
        hijos = st.radio("¿Tiene hijos? (Asignación Familiar)", ["No", "Sí"], horizontal=True)
        
        st.markdown("---")
        st.info(f"💡 Semestre: **{f_inicio.strftime('%d/%m/%Y')}** al **{f_corte.strftime('%d/%m/%Y')}**")
        
        fecha_inicio_real = max(fecha_ingreso, f_inicio)
        if fecha_inicio_real > f_corte:
            st.warning("⚠️ La fecha de ingreso está fuera del rango de este año.")
            meses_calc, dias_calc = 0, 0
        else:
            delta = f_corte - fecha_inicio_real
            total_dias = delta.days + 1
            meses_calc = total_dias // 30
            dias_calc = total_dias % 30
            if meses_calc > 6: meses_calc = 6; dias_calc = 0

        st.markdown(f"**Tiempo a computar:** `{meses_calc} meses` y `{dias_calc} días`.")
        btn_calcular = st.button(f"CALCULAR CTS {nombre_periodo.upper()}")

with col2:
    st.markdown(f"### 📊  Resultados Detallados")
    
    if btn_calcular:
        if sueldo <= 0:
            st.error("Por favor, ingresa un sueldo válido.")
        else:
            asig_fam = 113.00 if hijos == "Sí" else 0
            grati_sexto = sueldo / 6
            base_computable = sueldo + asig_fam + grati_sexto
            
            monto_meses = (base_computable / 12) * meses_calc
            monto_dias = (base_computable / 360) * dias_calc
            total_cts = monto_meses + monto_dias
            
            st.markdown(f"""
                <div class="result-card">
                    <h4 style='color: #94a3b8;'>Monto estimado para {nombre_periodo}:</h4>
                    <h1 style='color: #38bdf8; font-size: 50px;'>S/. {total_cts:,.2f}</h1>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Ver desglose técnico", expanded=True):
                st.write(f"**Sueldo Base:** S/. {sueldo:,.2f}")
                st.write(f"**Asignación Familiar:** S/. {asig_fam:,.2f}")
                st.write(f"**+ 1/6 Gratificación:** S/. {grati_sexto:,.2f}")
                st.write(f"**Base Computable:** S/. {base_computable:,.2f}")
                st.write(f"**Tiempo:** {meses_calc} meses y {dias_calc} días")
            
    else:
        st.info(f"Selecciona tus datos. Actualmente el sistema detecta el periodo de **{nombre_periodo}**.")
        
    # GUÍA INFORMATIVA
st.markdown("---")
col_seo1, col_seo2 = st.columns(2)

with col_seo1:
    st.markdown("### ❓ Guía rápida de la CTS 2026 en Perú")
    st.write("**¿Quiénes reciben CTS?**")
    st.write("Trabajadores del régimen laboral privado con jornada mínima de 4 horas.")
    st.write("**¿Cuándo se paga?**")
    st.write("Depósitos en la primera quincena de mayo y noviembre.")

with col_seo2:
    st.markdown("### ⚖️ Base Legal y Retiro")
    st.write("**Ley N.º 32322:** Esta ley autoriza el retiro del 100% de los fondos de CTS durante el año 2026.")
    st.write("**Disponibilidad:** El cálculo aquí mostrado es una simulación de lo que tu empleador debe depositar en tu cuenta bancaria.")    

# Pie de página
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #94a3b8;'>*Esta simulación es referencial - Periodo Actual: {nombre_periodo}.<br>© 2026 Calculadora de CTS Profesional</div></p>", unsafe_allow_html=True)
