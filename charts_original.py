"""
Módulo para crear gráficos y visualizaciones
"""
import plotly.express as px
import plotly.graph_objects as go
import folium
import pandas as pd
from config import MAP_CONFIG

def crear_grafico_distancias(estadisticas_df):
    """Crear gráfico de barras de distancias promedio"""
    fig = px.bar(
        estadisticas_df.sort_values('Distancia_Media'),
        x='Item',
        y='Distancia_Media',
        color='Departamento',
        title='📏 Distancia Promedio a las 10 Comunidades Más Cercanas por Granja',
        labels={
            'Distancia_Media': 'Distancia Promedio (km)',
            'Item': 'Granja (Item)'
        },
        hover_data=['Municipio', 'Distancia_Min', 'Distancia_Max'],
        height=500
    )
    
    fig.update_layout(
        xaxis_title="Granja",
        yaxis_title="Distancia (km)",
        showlegend=True,
        template="plotly_white"
    )
    
    return fig

def crear_histograma_distancias(resumen_detallado_df):
    """Crear histograma de distribución de distancias"""
    fig = px.histogram(
        resumen_detallado_df,
        x='Distancia_km',
        title='📊 Distribución de Distancias entre Granjas y Comunidades',
        labels={'Distancia_km': 'Distancia (km)', 'count': 'Frecuencia'},
        nbins=30,
        height=400
    )
    
    fig.update_layout(
        xaxis_title="Distancia (km)",
        yaxis_title="Frecuencia",
        template="plotly_white"
    )
    
    return fig

def crear_mapa_principal(granjas_df, comunidades_df):
    """Crear mapa principal con granjas y comunidades"""
    center = MAP_CONFIG["center_colombia"]
    mapa = folium.Map(
        location=center, 
        zoom_start=MAP_CONFIG["zoom_start"],
        tiles='OpenStreetMap'
    )
    
    # Agregar granjas
    for _, granja in granjas_df.iterrows():
        folium.Marker(
            location=[granja['Latitud'], granja['Longitud']],
            popup=f"""
            <b>Granja {granja['Item']}</b><br>
            📍 {granja['Municipio']}, {granja['Departamento']}<br>
            ⚡ {granja['Potencia  KW']} kW<br>
            👥 {granja['Beneficiarios']} beneficiarios
            """,
            tooltip=f"Granja {granja['Item']} - {granja['Municipio']}",
            icon=folium.Icon(color='red', icon='solar-panel', prefix='fa')
        ).add_to(mapa)
    
    # Agregar muestra de comunidades
    sample_size = min(MAP_CONFIG["folium_sample_size"], len(comunidades_df))
    comunidades_muestra = comunidades_df.sample(n=sample_size)
    
    for _, comunidad in comunidades_muestra.iterrows():
        if pd.notna(comunidad['x']) and pd.notna(comunidad['y']):
            folium.CircleMarker(
                location=[comunidad['y'], comunidad['x']],
                popup=f"""
                <b>ID {comunidad['ID']}</b><br>
                {comunidad['Nombre de la comunidad'][:50]}...<br>
                📍 {comunidad['Municipio']}, {comunidad['Departamento']}<br>
                ⚡ {comunidad['Potencia Estimada kWp']} kWp
                """,
                tooltip=f"CE {comunidad['ID']}",
                radius=3,
                color='blue',
                fillColor='lightblue',
                fillOpacity=0.6
            ).add_to(mapa)
    
    return mapa

def crear_mapa_scatter(granjas_df, comunidades_df):
    """Crear mapa scatter con Plotly"""
    fig = go.Figure()
    
    # Agregar granjas
    fig.add_trace(go.Scattermapbox(
        lat=granjas_df['Latitud'],
        lon=granjas_df['Longitud'],
        mode='markers',
        marker=dict(size=15, color='red', symbol='circle'),
        text=[f"Granja {row['Item']}<br>{row['Municipio']}, {row['Departamento']}" 
              for _, row in granjas_df.iterrows()],
        name='Granjas Solares',
        hovertemplate='<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
    ))
    
    # Agregar muestra de comunidades
    sample_size = min(MAP_CONFIG["comunidades_sample_size"], len(comunidades_df))
    comunidades_muestra = comunidades_df.sample(n=sample_size)
    fig.add_trace(go.Scattermapbox(
        lat=comunidades_muestra['y'],
        lon=comunidades_muestra['x'],
        mode='markers',
        marker=dict(size=6, color='blue', symbol='circle', opacity=0.6),
        text=[f"ID {row['ID']}<br>{row['Municipio']}, {row['Departamento']}" 
              for _, row in comunidades_muestra.iterrows()],
        name='Comunidades Energéticas',
        hovertemplate='<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
    ))
    
    center = MAP_CONFIG["center_colombia"]
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center[0], lon=center[1]),
            zoom=5
        ),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        title="��️ Ubicación de Granjas Solares y Comunidades Energéticas"
    )
    
    return fig
