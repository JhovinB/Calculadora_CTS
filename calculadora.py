import streamlit as st
from datetime import date

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Calculadora CTS Perú 2026", layout="wide")

# 2. CSS PARA DISEÑO MIDNIGHT
st.markdown("""
    <style>
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
    
    /* NUEVAS REGLAS PARA OCULTAR MENÚS Y FOOTER */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
    </style>
    """, unsafe_allow_html=True)
# Encabezado Dinámico
st.markdown(f"<h1 style='text-align: center;'>Calculadora CTS 2026</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Simulación precisa según Ley N.º 32322 (Retiro 100%)</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

# 3. LÓGICA DE DETECCIÓN INTELIGENTE
# Definimos los cortes fijos del año 2026
CORTE_MAYO = date(2026, 4, 30)
INICIO_MAYO = date(2025, 11, 1)

CORTE_NOVIEMBRE = date(2026, 10, 31)
INICIO_NOVIEMBRE = date(2026, 5, 1)

# --- INICIO DE LA INTERFAZ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Ingreso de Datos")
    with st.container(border=True):
        # El usuario elige fecha
        fecha_ingreso = st.date_input("Fecha de Ingreso Laboral", value=date(2026, 1, 1))
        
        # --- CÁLCULO DINÁMICO ---
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
        
        # Cálculo de tiempo dentro del semestre seleccionado
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

# Pie de página
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #94a3b8;'>*Esta simulación es referencial - Periodo Actual: {nombre_periodo}.<br>© 2026 Calculadora de CTS Profesional</div></p>", unsafe_allow_html=True)