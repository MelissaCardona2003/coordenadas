"""
Componentes de la interfaz de usuario
"""
import streamlit as st

def render_header():
    """Renderizar header principal"""
    st.markdown("""
    <div class="main-header">
        <h1>☀️ Análisis de Proximidad - Granjas Solares y Comunidades Energéticas</h1>
        <h3>Las 10 Comunidades Energéticas Más Cercanas por Granja</h3>
        <p>Ministerio de Minas y Energías - Colombia</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_metrics(granjas_actualizadas, comunidades, estadisticas):
    """Renderizar métricas del sidebar"""
    st.sidebar.markdown("### 📈 Métricas Clave")
    st.sidebar.metric("Total Granjas", len(granjas_actualizadas))
    st.sidebar.metric("Total Comunidades", len(comunidades))
    st.sidebar.metric("Distancia Promedio", f"{estadisticas['Distancia_Media'].mean():.2f} km")
    st.sidebar.metric("Distancia Mínima", f"{estadisticas['Distancia_Min'].min():.2f} km")

def render_main_metrics(granjas_actualizadas, comunidades, estadisticas):
    """Renderizar métricas principales"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Granjas Analizadas",
            value=len(granjas_actualizadas),
            delta=f"{len(comunidades)} comunidades disponibles"
        )
    
    with col2:
        st.metric(
            label="Distancia Promedio",
            value=f"{estadisticas['Distancia_Media'].mean():.2f} km",
            delta=f"±{estadisticas['Distancia_Media'].std():.2f}"
        )
    
    with col3:
        mejor_granja = estadisticas.loc[estadisticas['Distancia_Media'].idxmin()]
        st.metric(
            label="Mejor Ubicación",
            value=f"Granja {mejor_granja['Item']}",
            delta=f"{mejor_granja['Distancia_Media']:.2f} km promedio"
        )
    
    with col4:
        peor_granja = estadisticas.loc[estadisticas['Distancia_Media'].idxmax()]
        st.metric(
            label="Mayor Desafío",
            value=f"Granja {peor_granja['Item']}",
            delta=f"{peor_granja['Distancia_Media']:.2f} km promedio",
            delta_color="inverse"
        )

def render_granja_info(granja_info, stats_granja):
    """Renderizar información detallada de una granja"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **🏗️ Granja {granja_info['Item']}**
        - **📍 Ubicación**: {granja_info['Municipio']}, {granja_info['Departamento']}
        - **⚡ Potencia**: {granja_info['Potencia  KW']} kW
        - **👥 Beneficiarios**: {granja_info['Beneficiarios']}
        - **🗂️ Fuente**: {granja_info['Fuente de financiamiento']}
        """)
    
    with col2:
        st.markdown(f"""
        **📊 Estadísticas de Proximidad**
        - **📐 Distancia Mínima**: {stats_granja['Distancia_Min']:.2f} km
        - **📏 Distancia Promedio**: {stats_granja['Distancia_Media']:.2f} km
        - **📈 Distancia Máxima**: {stats_granja['Distancia_Max']:.2f} km
        """)

def render_download_buttons(dataframe, filename_base, label_prefix="Descargar"):
    """Renderizar botones de descarga para CSV y Excel"""
    from data_loader import to_excel
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label=f"📥 {label_prefix} CSV",
            data=dataframe.to_csv(index=False),
            file_name=f"{filename_base}.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_data = to_excel(dataframe)
        st.download_button(
            label=f"📊 {label_prefix} Excel",
            data=excel_data,
            file_name=f"{filename_base}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def render_footer():
    """Renderizar footer del dashboard"""
    st.markdown("---")
    st.markdown("""
    <div class="footer-style">
        <h3>💡 Dashboard Desarrollado para el Ministerio de Energías</h3>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            📊 Análisis de proximidad entre granjas solares y comunidades energéticas<br>
            🔬 <strong>Datos procesados:</strong> 15 granjas solares × 17,518 comunidades energéticas<br>
            📏 <strong>Algoritmo:</strong> Cálculo de distancias geodésicas con precisión geoespacial
        </p>
        <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #404040;">
            <span style="color: #FFD23F;">⚡ Energía Renovable</span> • 
            <span style="color: #FF6B35;">☀️ Futuro Sostenible</span> • 
            <span style="color: #00D9FF;">🌱 Colombia Verde</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
