"""
Dashboard Principal ESTABLE - Granjas Solares y Comunidades Energéticas
Con mapa Folium optimizado y estable
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Dashboard - Granjas Solares y Comunidades Energéticas",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS optimizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-color: #FF6B35;
        --secondary-color: #FFD23F;
        --accent-color: #F18F01;
        --success-color: #00D9FF;
        --bg-dark: #0A0A0A;
        --bg-card: #1A1A1A;
        --text-primary: #FFFFFF;
        --text-secondary: #E5E5E5;
        --border: #333333;
    }
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: var(--bg-dark);
        color: var(--text-primary);
    }
    
    .main-header {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid var(--border);
    }
    
    h1 { font-family: 'Poppins', sans-serif; color: var(--primary-color); }
    h2 { color: var(--text-primary); }
    h3 { color: var(--accent-color); }
    
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    """Cargar todos los datasets necesarios"""
    try:
        granjas_actualizadas = pd.read_csv('Base granjas_actualizada.csv')
        comunidades = pd.read_csv('Base comunidades energéticas.csv')
        estadisticas = pd.read_csv('estadisticas_distancias.csv')
        resumen_detallado = pd.read_csv('resumen_detallado_proximidades.csv')
        
        return granjas_actualizadas, comunidades, estadisticas, resumen_detallado
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None, None

@st.cache_data(ttl=3600)
def crear_mapa_estable(_granjas_df, _comunidades_df):
    """Crear mapa Folium ESTABLE y optimizado"""
    
    # Mapa base optimizado
    mapa = folium.Map(
        location=[4.5, -74],
        zoom_start=6,
        tiles='OpenStreetMap',
        prefer_canvas=True,
        max_zoom=15,
        min_zoom=4
    )
    
    # Agregar granjas con marcadores estables
    for _, granja in _granjas_df.iterrows():
        if pd.notna(granja['Latitud']) and pd.notna(granja['Longitud']):
            lat, lon = float(granja['Latitud']), float(granja['Longitud'])
            if -5 <= lat <= 15 and -85 <= lon <= -65:  # Validar coordenadas Colombia
                
                popup_html = f"""
                <div style="font-family: Arial; max-width: 200px; padding: 8px;">
                    <b style="color: #FF6B35;">🏗️ Granja {granja['Item']}</b><br>
                    📍 {granja['Municipio']}, {granja['Departamento']}<br>
                    ⚡ {granja['Potencia  KW']} kW<br>
                    👥 {granja['Beneficiarios']} beneficiarios
                </div>
                """
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=220),
                    tooltip=f"Granja {granja['Item']}",
                    icon=folium.Icon(color='red', icon='bolt', prefix='fa')
                ).add_to(mapa)
    
    # Agregar comunidades con clustering
    cluster = MarkerCluster(
        options={'maxClusterRadius': 40, 'spiderfyOnMaxZoom': True}
    )
    
    # Muestra muy pequeña para máxima estabilidad
    sample_size = min(25, len(_comunidades_df))
    comunidades_muestra = _comunidades_df.sample(n=sample_size, random_state=42)
    
    for _, comunidad in comunidades_muestra.iterrows():
        if pd.notna(comunidad['x']) and pd.notna(comunidad['y']):
            try:
                lat, lon = float(comunidad['y']), float(comunidad['x'])
                if -5 <= lat <= 15 and -85 <= lon <= -65:
                    
                    popup_html = f"""
                    <div style="font-family: Arial; max-width: 180px; padding: 6px;">
                        <b style="color: #00D9FF;">⚡ CE {comunidad['ID']}</b><br>
                        {str(comunidad['Nombre de la comunidad'])[:30]}...<br>
                        📍 {comunidad['Municipio']}<br>
                        ⚡ {comunidad['Potencia Estimada kWp']} kWp
                    </div>
                    """
                    
                    folium.CircleMarker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_html, max_width=200),
                        tooltip=f"CE {comunidad['ID']}",
                        radius=4,
                        color='#00D9FF',
                        fillColor='#00D9FF',
                        fillOpacity=0.7,
                        weight=2
                    ).add_to(cluster)
            except:
                continue
    
    cluster.add_to(mapa)
    
    return mapa

def crear_mapa_plotly(_granjas_df, _comunidades_df):
    """Crear mapa Plotly más estable"""
    fig = go.Figure()
    
    # Granjas
    fig.add_trace(go.Scattermapbox(
        lat=_granjas_df['Latitud'],
        lon=_granjas_df['Longitud'],
        mode='markers',
        marker=dict(size=15, color='#FF6B35'),
        text=[f"Granja {row['Item']}<br>{row['Municipio']}, {row['Departamento']}" 
              for _, row in _granjas_df.iterrows()],
        name='🏗️ Granjas Solares',
        hovertemplate='%{text}<extra></extra>'
    ))
    
    # Comunidades - muestra filtrada
    sample_size = min(80, len(_comunidades_df))
    comunidades_muestra = _comunidades_df.sample(n=sample_size, random_state=42)
    
    # Filtrar coordenadas válidas
    comunidades_validas = comunidades_muestra[
        (comunidades_muestra['y'].notna()) & 
        (comunidades_muestra['x'].notna()) &
        (comunidades_muestra['y'] >= -5) & 
        (comunidades_muestra['y'] <= 15) &
        (comunidades_muestra['x'] >= -85) & 
        (comunidades_muestra['x'] <= -65)
    ]
    
    if len(comunidades_validas) > 0:
        fig.add_trace(go.Scattermapbox(
            lat=comunidades_validas['y'],
            lon=comunidades_validas['x'],
            mode='markers',
            marker=dict(size=8, color='#00D9FF', opacity=0.7),
            text=[f"CE {row['ID']}<br>{row['Municipio']}" 
                  for _, row in comunidades_validas.iterrows()],
            name='⚡ Comunidades Energéticas',
            hovertemplate='%{text}<extra></extra>'
        ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=4.5, lon=-74),
            zoom=6
        ),
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
        title="🗺️ Ubicación de Granjas y Comunidades Energéticas"
    )
    
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>☀️ Análisis de Proximidad - Granjas Solares y Comunidades Energéticas</h1>
        <h3>Las 10 Comunidades Energéticas Más Cercanas por Granja</h3>
        <p>Ministerio de Minas y Energías - Colombia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cargar datos
    with st.spinner('🔄 Cargando datos...'):
        granjas_actualizadas, comunidades, estadisticas, resumen_detallado = cargar_datos()
    
    if granjas_actualizadas is None:
        st.error("❌ No se pudieron cargar los datos.")
        return
    
    # Sidebar
    st.sidebar.markdown("### 🔧 Navegación")
    vista = st.sidebar.selectbox(
        "Selecciona la vista:",
        ["🔍 Explorar por Granja", "🗺️ Mapas Interactivos", "📈 Estadísticas", "📋 Datos"]
    )
    
    # Métricas sidebar
    st.sidebar.markdown("### 📈 Métricas")
    st.sidebar.metric("Granjas", len(granjas_actualizadas))
    st.sidebar.metric("Comunidades", len(comunidades))
    st.sidebar.metric("Dist. Promedio", f"{estadisticas['Distancia_Media'].mean():.1f} km")
    
    # Contenido principal
    if vista == "🔍 Explorar por Granja":
        st.markdown("## 🔍 Explorador por Granja")
        
        st.info("🎯 Identificar las 10 comunidades energéticas más cercanas a cada granja solar.")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Granjas Analizadas", len(granjas_actualizadas))
        with col2:
            st.metric("Distancia Promedio", f"{estadisticas['Distancia_Media'].mean():.2f} km")
        with col3:
            mejor = estadisticas.loc[estadisticas['Distancia_Media'].idxmin()]
            st.metric("Mejor Ubicación", f"Granja {mejor['Item']}")
        with col4:
            peor = estadisticas.loc[estadisticas['Distancia_Media'].idxmax()]
            st.metric("Mayor Desafío", f"Granja {peor['Item']}")
        
        st.markdown("---")
        
        # Selector de granja
        granja_seleccionada = st.selectbox(
            "Selecciona una granja:",
            options=granjas_actualizadas['Item'].tolist(),
            format_func=lambda x: f"Granja {x} - {granjas_actualizadas[granjas_actualizadas['Item']==x]['Municipio'].iloc[0]}"
        )
        
        if granja_seleccionada:
            granja_info = granjas_actualizadas[granjas_actualizadas['Item'] == granja_seleccionada].iloc[0]
            stats_granja = estadisticas[estadisticas['Item'] == granja_seleccionada].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **🏗️ Granja {granja_seleccionada}**
                - **📍 Ubicación**: {granja_info['Municipio']}, {granja_info['Departamento']}
                - **⚡ Potencia**: {granja_info['Potencia  KW']} kW
                - **👥 Beneficiarios**: {granja_info['Beneficiarios']}
                """)
            
            with col2:
                st.markdown(f"""
                **📊 Estadísticas**
                - **📐 Dist. Mínima**: {stats_granja['Distancia_Min']:.2f} km
                - **📏 Dist. Promedio**: {stats_granja['Distancia_Media']:.2f} km
                - **📈 Dist. Máxima**: {stats_granja['Distancia_Max']:.2f} km
                """)
            
            # Tabla de comunidades cercanas
            st.markdown(f"#### 🎯 Las 10 Comunidades Más Cercanas a Granja {granja_seleccionada}")
            
            comunidades_detalle = resumen_detallado[
                resumen_detallado['Granja_Item'] == granja_seleccionada
            ].sort_values('Ranking')[['Ranking', 'Comunidad_ID', 'Comunidad_Nombre', 
                                     'Comunidad_Municipio', 'Distancia_km']]
            
            st.dataframe(comunidades_detalle, hide_index=True, use_container_width=True)
    
    elif vista == "🗺️ Mapas Interactivos":
        st.markdown("## 🗺️ Mapas Interactivos")
        
        tab1, tab2 = st.tabs(["🗺️ Mapa Estable (Folium)", "📍 Mapa Plotly"])
        
        with tab1:
            st.markdown("### 🗺️ Mapa Interactivo Optimizado")
            st.info("🔴 **Granjas Solares** | 🔵 **Comunidades Energéticas** (muestra reducida para estabilidad)")
            
            with st.spinner("🔄 Generando mapa estable..."):
                mapa = crear_mapa_estable(granjas_actualizadas, comunidades)
                st_folium(mapa, width=700, height=500, returned_objects=["last_object_clicked"])
        
        with tab2:
            st.markdown("### 📍 Mapa de Dispersión")
            fig_plotly = crear_mapa_plotly(granjas_actualizadas, comunidades)
            st.plotly_chart(fig_plotly, use_container_width=True)
    
    elif vista == "📈 Estadísticas":
        st.markdown("## 📈 Estadísticas Detalladas")
        
        # Top granjas
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🏆 Top 5 Mejores Ubicaciones")
            top_5 = estadisticas.nsmallest(5, 'Distancia_Media')[['Item', 'Municipio', 'Distancia_Media']]
            st.dataframe(top_5, hide_index=True)
        
        with col2:
            st.markdown("### ⚠️ Top 5 Mayores Desafíos") 
            bottom_5 = estadisticas.nlargest(5, 'Distancia_Media')[['Item', 'Municipio', 'Distancia_Media']]
            st.dataframe(bottom_5, hide_index=True)
        
        # Gráfico de distancias
        fig = px.bar(
            estadisticas.sort_values('Distancia_Media'),
            x='Item', y='Distancia_Media',
            color='Departamento',
            title='📏 Distancia Promedio a las 10 Comunidades Más Cercanas',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif vista == "📋 Datos":
        st.markdown("## 📋 Datos y Tablas")
        
        tab1, tab2 = st.tabs(["🎯 Tabla Principal", "📊 Todas las Bases"])
        
        with tab1:
            st.markdown("### 🎯 Tabla Principal del Análisis")
            
            # Crear tabla principal
            tabla_principal = []
            for _, granja in granjas_actualizadas.iterrows():
                item = granja['Item']
                ces_ids = granja['CEs Relacionadas'] 
                stats = estadisticas[estadisticas['Item'] == item].iloc[0]
                
                tabla_principal.append({
                    'Granja': f"Granja {item}",
                    'Ubicación': f"{granja['Municipio']}, {granja['Departamento']}",
                    'Potencia_kW': granja['Potencia  KW'],
                    'IDs_10_CEs_Cercanas': ces_ids,
                    'Distancia_Promedio_km': round(stats['Distancia_Media'], 2),
                    'Beneficiarios': granja['Beneficiarios']
                })
            
            df_principal = pd.DataFrame(tabla_principal)
            st.dataframe(df_principal, hide_index=True, use_container_width=True)
            
            # Botón descarga
            csv = df_principal.to_csv(index=False)
            st.download_button("📥 Descargar CSV", csv, "tabla_principal.csv", "text/csv")
        
        with tab2:
            st.markdown("### 📊 Base de Granjas")
            st.dataframe(granjas_actualizadas, hide_index=True)
            
            st.markdown("### ⚡ Comunidades Energéticas (muestra)")
            st.dataframe(comunidades.head(50), hide_index=True) 
            st.info(f"Mostrando 50 de {len(comunidades)} comunidades")

if __name__ == "__main__":
    main()
