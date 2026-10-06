import streamlit as st
import math

# 1. CONFIGURACIÓN DE LA APP (Marca unificada YAR)
st.set_page_config(page_title="YAR Zapatas", page_icon="🏗️", layout="centered")

st.title("🧱 YAR Structural - Zapatas Aisladas")
st.write("Predimensionamiento normativo automatizado en planta de zapatas céntricas según la clasificación de suelos del RNE.")
st.write("---")

st.subheader("Esquema Geométrico en Planta de Cimentación")

zapata_planta_svg = """
<svg xmlns="http://w3.org" viewBox="0 0 600 240" width="100%">
  <rect width="600" height="240" fill="#11151c" rx="10"/>
  <rect x="180" y="30" width="240" height="180" fill="#4a5568" stroke="#cbd5e1" stroke-width="2"/>
  <rect x="270" y="95" width="60" height="50" fill="#1e293b" stroke="#f8fafc" stroke-width="1.5"/>
  <line x1="300" y1="15" x2="300" y2="225" stroke="#e11d48" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="150" y1="120" x2="450" y2="120" stroke="#e11d48" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="180" y1="225" x2="420" y2="225" stroke="#38bdf8" stroke-width="1.5"/>
  <polyline points="190,221 180,225 190,229" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
  <polyline points="410,221 420,225 410,229" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="295" y="238" fill="#38bdf8" font-family="Arial" font-size="14" font-weight="bold">L</text>
  <line x1="160" y1="30" x2="160" y2="210" stroke="#38bdf8" stroke-width="1.5"/>
  <polyline points="156,40 160,30 164,40" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
  <polyline points="156,200 160,210 164,200" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="140" y="125" fill="#38bdf8" font-family="Arial" font-size="14" font-weight="bold">B</text>
  <text x="430" y="50" fill="#f8fafc" font-family="Arial" font-size="12" font-weight="bold">Zapata (B x L)</text>
  <text x="340" y="110" fill="#f8fafc" font-family="Arial" font-size="12" font-weight="bold">Columna (b x t)</text>
</svg>
"""
st.markdown(zapata_planta_svg, unsafe_allow_html=True)
st.write("---")

st.subheader("Datos de Entrada")

p_muerta = st.number_input("Carga Muerta actuante de la columna PD (Toneladas)", min_value=1.0, max_value=500.0, value=50.0, step=5.0)
p_viva = st.number_input("Carga Viva actuante de la columna PL (Toneladas)", min_value=1.0, max_value=300.0, value=15.0, step=5.0)
sigma_adm = st.number_input("Capacidad Portante Admisible del Suelo σadm (kg/cm²)", min_value=0.1, max_value=10.0, value=1.5, step=0.1)

st.write("**Sección de la Columna de Apoyo:**")
col_b = st.number_input("Ancho de la columna 'b' (metros)", min_value=0.20, max_value=2.00, value=0.40, step=0.05)
col_t = st.number_input("Largo de la columna 't' (metros)", min_value=0.20, max_value=2.00, value=0.50, step=0.05)

# Clasificación automática según el valor de capacidad portante admisible de tu imagen
if sigma_adm > 1.0:
    k_diseno, suelo_txt, h_zapata = 0.9, "S1: RIGIDO", "0.40 m"
elif 0.5 <= sigma_adm <= 1.0:
    k_diseno, suelo_txt, h_zapata = 0.8, "S2: INTERMEDIO", "0.50 m"
else:
    k_diseno, suelo_txt, h_zapata = 0.7, "S3: FLEXIBLE O BLANDO", "Plateas o losas de cimentación"

# Muestra en tiempo real la detección automática del suelo al usuario
st.info(f"💡 **Clasificación Automatizada:** Suelo detectado como **{suelo_txt}** (K = {k_diseno}) según el valor de capacidad portante ingresado.")

if st.button("Calcular Zapata Aislada ▶️", use_container_width=True):
    sigma_adm_ton = sigma_adm * 10.0
    p_servicio_total = p_muerta + p_viva
    
    # FÓRMULA DE TU IMAGEN: Az = Pservicio / (K * qadm)
    area_requerida = p_servicio_total / (k_diseno * sigma_adm_ton)
    
    diff_col = col_t - col_b
    discriminante = (diff_col ** 2) + (4 * area_requerida)
    
    if discriminante >= 0:
        b_calculado = (-diff_col + math.sqrt(discriminante)) / 2.0
        l_calculado = area_requerida / b_calculado
        b_final = math.ceil(b_calculado * 10) / 10.0
        l_final = math.ceil(l_calculado * 10) / 10.0
    else:
        b_final = math.ceil(math.sqrt(area_requerida) * 10) / 10.0
        l_final = b_final

    area_disenada = b_final * l_final
    q_real_suelo = p_servicio_total / area_disenada
    condicion_geotecnica = "CONFORME (OK)" if q_real_suelo <= sigma_adm_ton else "REDISEÑAR"

    if "S3" in suelo_txt:
        st.warning("⚠️ **Recomendación Especial:** Según tu tabla, para suelos S3 flexibles se recomienda evaluar Plateas o Losas de cimentación en lugar de zapatas aisladas.")

    st.success("### 📊 CÁLCULO COMPLETADO CON TU TABLA")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(label="📐 Ancho Comercial (B)", value=f"{b_final:.2f} m")
    with col_res2:
        st.metric(label="📐 Largo Comercial (L)", value=f"{l_final:.2f} m")

    st.write("---")
    
    css_ajuste = """<style>div[data-testid="stMarkdownContainer"]{width:100%!important;overflow-x:hidden!important;}.hoja-blanca{background-color:white!important;color:#111!important;padding:25px!important;border:2px solid #222!important;border-radius:8px!important;font-family:Arial,sans-serif!important;width:100%!important;max-width:100%!important;box-sizing:border-box!important;word-wrap:break-word!important;word-break:break-word!important;}</style>"""
    st.markdown(css_ajuste, unsafe_allow_html=True)
    
    # REPORTE EN HOJA BLANCA TOTALMENTE ACOPLADO CON IMPRESIÓN DIRECTA
    reporte_html = "<div class='hoja-blanca'>"
    reporte_html += "<h2 style='text-align:center; color:#1e3a8a; font-weight:bold; margin:0 0 5px 0; font-size:20px;'>MEMORIA DE CÁLCULO ESTRUCTURAL</h2>"
    reporte_html += "<p style='text-align:center; color:#111111; font-weight:bold; margin:0 0 10px 0; font-size:14px;'>SOFTWARE: YAR STRUCTURAL</p>"
    reporte_html += "<hr style='border:0; border-top:1px solid #333; margin-bottom:15px;'>"
    
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'><strong>Consultor estructural:</strong> Ing. Yhoel Aquino Reyes</p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'><strong>Elemento:</strong> Zapata Aislada Céntrica Rectangular</p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'><strong>Normativa aplicada:</strong> Reglamento Nacional de Edificaciones (RNE - Perú)</p>"
    
    reporte_html += "<h4 style='color:#1e3a8a; margin-top:18px; margin-bottom:6px; border-bottom:1px solid #ddd; padding-bottom:4px; font-size:15px;'>1. PARÁMETROS DE DISEÑO (ENTRADA)</h4>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• <strong>Carga de Servicio (P<sub>servicio</sub>):</strong> {p_servicio_total:.2f} Toneladas</p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• <strong>Carga Admisible del Terreno (q<sub>adm</sub>):</strong> {sigma_adm:.2f} kg/cm² ({sigma_adm_ton:.1f} Tn/m²)</p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• <strong>Factor de Diseño (K) Determinado:</strong> {k_diseno:.2f}</p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• <strong>Clasificación del Suelo (Tabla EMS):</strong> {suelo_txt}</p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• <strong>Sección de la Columna de Apoyo:</strong> {col_b:.2f}m x {col_t:.2f}m</p>"
    
    reporte_html += "<h4 style='color:#1e3a8a; margin-top:18px; margin-bottom:6px; border-bottom:1px solid #ddd; padding-bottom:4px; font-size:15px;'>2. PROCEDIMIENTO DETALLADO DE CÁLCULO</h4>"
    reporte_html += f"<p style='color:#111111; margin:6px 0; font-size:14px;'><strong>Ecuación Utilizada:</strong><br><span style='color:#b91c1c; font-weight:bold;'>A<sub>zapata</sub> = P<sub>servicio</sub> / (K &times; q<sub>adm</sub>)</span></p>"
    reporte_html += f"<p style='color:#111111; margin:6px 0; font-size:14px;'><strong>Sustitución de Valores:</strong><br>A<sub>z</sub> = {p_servicio_total:.2f} / ({k_diseno:.2f} &times; {sigma_adm_ton:.1f}) = <strong>{area_requerida:.3f} m²</strong></p>"
    
    reporte_html += "<h4 style='color:#1e3a8a; margin-top:18px; margin-bottom:6px; border-bottom:1px solid #ddd; padding-bottom:4px; font-size:15px;'>3. CONCLUSIÓN Y DIMENSIONAMIENTO CONSTRUCTIVO</h4>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• Dimensiones en Planta Recomendadas: <strong>{b_final:.2f} m x {l_final:.2f} m</strong></p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• Área Final Dispuesta (A<sub>z</sub>): <strong>{area_disenada:.2f} m²</strong></p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• <strong>Altura Mínima de Zapata Recomendada (Peralte hz):</strong> {h_zapata}</p>"
    reporte_html += f"<p style='color:#111111; margin:6px 0; font-size:14px;'>• <strong>Presión Actuante Real (q<sub>real</sub>):</strong><br>q<sub>real</sub> = P<sub>servicio</sub> / A<sub>diseñada</sub><br>q<sub>real</sub> = {p_servicio_total:.2f} / {area_disenada:.2f} = {q_real_suelo:.3f} Tn/m² &rarr; <strong>{q_real_suelo / 10.0:.3f} kg/cm²</strong></p>"
    reporte_html += f"<p style='color:#111111; margin:4px 0; font-size:14px;'>• Verificación de Esfuerzos Final: <strong>{condicion_geotecnica}</strong></p>"
    
    reporte_html += "<hr style='border:0; border-top:1px solid #333; margin-top:20px; margin-bottom:10px;'>"
    reporte_html += "<p style='text-align:center; font-size:11px; font-style:italic; color:#555; margin:0;'>Memoria técnica generada automáticamente por YAR Structural. Conforme al RNE Perú.</p>"
    reporte_html += "</div>"
    
    st.markdown(reporte_html, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🖨️ Exportar Memoria de Cálculo a PDF / Imprimir", use_container_width=True):
       
