"""
Vistas del dashboard
"""
import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from components import render_main_metrics, render_granja_info, render_download_buttons
from charts import crear_grafico_distancias, crear_histograma_distancias, crear_mapa_principal_estable, crear_mapa_scatter
from data_loader import crear_tabla_principal

def vista_explorar_granja(granjas_actualizadas, estadisticas, resumen_detallado, comunidades):
    """Vista para explorar por granja"""
    st.markdown("## 🔍 Explorador por Granja")
    
    # Mensaje explicativo principal
    st.info("""
    🎯 **OBJETIVO PRINCIPAL**: Identificar las 10 comunidades energéticas más cercanas a cada granja solar 
    para facilitar la implementación y conexión por parte del Ministerio de Energías.
    """)
    
    # Métricas principales
    render_main_metrics(granjas_actualizadas, {}, estadisticas)
    
    st.markdown("---")
    
    # Selector de granja
    granja_detalle = st.selectbox(
        "Selecciona una granja para ver el detalle completo de sus 10 CEs más cercanas:",
        options=granjas_actualizadas['Item'].tolist(),
        format_func=lambda x: f"Granja {x} - {granjas_actualizadas[granjas_actualizadas['Item']==x]['Municipio'].iloc[0]}, {granjas_actualizadas[granjas_actualizadas['Item']==x]['Departamento'].iloc[0]}"
    )
    
    if granja_detalle:
        # Mostrar información detallada
        granja_info = granjas_actualizadas[granjas_actualizadas['Item'] == granja_detalle].iloc[0]
        stats_granja = estadisticas[estadisticas['Item'] == granja_detalle].iloc[0]
        
        render_granja_info(granja_info, stats_granja)
        
        # Tabla detallada de las 10 comunidades
        st.markdown(f"#### 🎯 Las 10 Comunidades Energéticas Más Cercanas a Granja {granja_detalle}")
        
        comunidades_detalle = resumen_detallado[
            resumen_detallado['Granja_Item'] == granja_detalle
        ].sort_values('Ranking')[['Ranking', 'Comunidad_ID', 'Comunidad_Nombre', 
                                 'Comunidad_Municipio', 'Comunidad_Departamento', 
                                 'Distancia_km', 'Potencia_kWp']]
        
        st.dataframe(
            comunidades_detalle,
            column_config={
                "Ranking": st.column_config.NumberColumn("🏆 #", width="small"),
                "Comunidad_ID": st.column_config.NumberColumn("🆔 ID CE", width="small"),
                "Comunidad_Nombre": st.column_config.TextColumn("📋 Nombre de la Comunidad", width="large"),
                "Comunidad_Municipio": st.column_config.TextColumn("🏘️ Municipio", width="medium"),
                "Comunidad_Departamento": st.column_config.TextColumn("🗺️ Departamento", width="medium"),
                "Distancia_km": st.column_config.NumberColumn("📏 Distancia (km)", width="small", format="%.2f"),
                "Potencia_kWp": st.column_config.NumberColumn("⚡ Potencia (kWp)", width="small")
            },
            hide_index=True,
            use_container_width=True
        )

def vista_mapas(granjas_actualizadas, comunidades):
    """Vista de mapas interactivos"""
    st.markdown("## 🗺️ Mapas Interactivos")
    
    tab1, tab2 = st.tabs(["🗺️ Mapa Folium", "📍 Mapa Plotly"])
    
    with tab1:
        st.markdown("### Mapa Interactivo con Folium")
        st.markdown("🔴 **Granjas Solares** | 🔵 **Comunidades Energéticas (muestra)**")
        
        mapa = crear_mapa_principal_estable(granjas_actualizadas, comunidades)
        st_folium(mapa, width=700, height=500)
    
    with tab2:
        st.markdown("### Mapa de Dispersión con Plotly")
        fig_scatter = crear_mapa_scatter(granjas_actualizadas, comunidades)
        st.plotly_chart(fig_scatter, use_container_width=True)

def vista_estadisticas(granjas_actualizadas, estadisticas, resumen_detallado, comunidades):
    """Vista de estadísticas detalladas"""
    st.markdown("## 📈 Estadísticas Detalladas")
    
    # Métricas principales
    render_main_metrics(granjas_actualizadas, comunidades, estadisticas)
    
    st.markdown("---")
    
    # Top y bottom granjas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top 5 Mejores Ubicaciones")
        top_5 = estadisticas.nsmallest(5, 'Distancia_Media')[['Item', 'Municipio', 'Departamento', 'Distancia_Media']]
        st.dataframe(top_5, hide_index=True)
    
    with col2:
        st.markdown("### ⚠️ Top 5 Mayores Desafíos")
        bottom_5 = estadisticas.nlargest(5, 'Distancia_Media')[['Item', 'Municipio', 'Departamento', 'Distancia_Media']]
        st.dataframe(bottom_5, hide_index=True)
    
    # Gráficos
    st.plotly_chart(crear_grafico_distancias(estadisticas), use_container_width=True)
    st.plotly_chart(crear_histograma_distancias(resumen_detallado), use_container_width=True)

def vista_datos_tablas(granjas_actualizadas, comunidades, estadisticas, resumen_detallado):
    """Vista de datos y tablas"""
    st.markdown("## 📋 Bases de Datos y Exportación")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Tabla Principal", "🏗️ Granjas", "⚡ Comunidades", 
        "📊 Estadísticas", "🔗 Relaciones Detalladas"
    ])
    
    with tab1:
        st.markdown("### 🎯 Tabla Principal: Granjas y sus 10 Comunidades Energéticas Más Cercanas")
        st.markdown("Esta es la tabla principal del análisis con los resultados solicitados por el Ministerio de Energías.")
        
        df_principal = crear_tabla_principal(granjas_actualizadas, estadisticas)
        
        st.dataframe(
            df_principal,
            column_config={
                "Granja": st.column_config.TextColumn("🏗️ Granja", width="small"),
                "Ubicación": st.column_config.TextColumn("📍 Ubicación", width="medium"),
                "Potencia_kW": st.column_config.NumberColumn("⚡ Potencia (kW)", width="small"),
                "IDs_10_CEs_Mas_Cercanas": st.column_config.TextColumn("🎯 IDs de 10 CEs Más Cercanas", width="large"),
                "Distancia_Promedio_km": st.column_config.NumberColumn("📏 Dist. Promedio (km)", width="small", format="%.2f"),
                "Distancia_Minima_km": st.column_config.NumberColumn("📐 Dist. Mínima (km)", width="small", format="%.2f"),
                "Beneficiarios": st.column_config.NumberColumn("👥 Beneficiarios", width="small")
            },
            hide_index=True,
            use_container_width=True
        )
        
        render_download_buttons(df_principal, "Tabla_Principal_Granjas_10_CEs_Cercanas", "Descargar Tabla Principal")
    
    with tab2:
        st.markdown("### 🏗️ Base de Granjas Actualizada")
        st.dataframe(granjas_actualizadas)
        render_download_buttons(granjas_actualizadas, "granjas_actualizadas")
    
    with tab3:
        st.markdown("### ⚡ Comunidades Energéticas")
        st.dataframe(comunidades.head(100))
        st.info(f"Mostrando 100 de {len(comunidades)} comunidades energéticas")
        render_download_buttons(comunidades, "comunidades_energeticas")
    
    with tab4:
        st.markdown("### 📊 Estadísticas por Granja")
        st.dataframe(estadisticas)
        render_download_buttons(estadisticas, "estadisticas_distancias")
    
    with tab5:
        st.markdown("### 🔗 Resumen Detallado de Relaciones")
        st.dataframe(resumen_detallado)
        render_download_buttons(resumen_detallado, "resumen_detallado_proximidades")
