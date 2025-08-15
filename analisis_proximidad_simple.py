#!/usr/bin/env python3
"""
Análisis de proximidad entre granjas solares y comunidades energéticas.
Identifica las 10 comunidades energéticas más cercanas a cada granja.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en kilómetros entre dos puntos usando la fórmula de Haversine.
    """
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def encontrar_comunidades_cercanas(granjas_df, comunidades_df, n_cercanas=10):
    """
    Encuentra las n comunidades energéticas más cercanas a cada granja.
    """
    resultados = []
    
    for idx_granja, granja in granjas_df.iterrows():
        lat_granja = granja['Latitud']
        lon_granja = granja['Longitud']
        
        # Calcular distancias a todas las comunidades
        distancias = []
        for idx_comunidad, comunidad in comunidades_df.iterrows():
            lat_comunidad = comunidad['y']
            lon_comunidad = comunidad['x']
            
            distancia = calcular_distancia_haversine(
                lat_granja, lon_granja, 
                lat_comunidad, lon_comunidad
            )
            
            distancias.append({
                'ID_Comunidad': comunidad['ID'],
                'Nombre_Comunidad': comunidad['Nombre de la comunidad'],
                'Departamento_Comunidad': comunidad['Departamento'],
                'Municipio_Comunidad': comunidad['Municipio'],
                'Distancia_km': distancia,
                'Potencia_kWp': comunidad['Potencia Estimada kWp'],
                'Inversion_Estimada': comunidad['Inversión Estimada']
            })
        
        # Ordenar por distancia y tomar las n más cercanas
        distancias_ordenadas = sorted(distancias, key=lambda x: x['Distancia_km'])
        n_mas_cercanas = distancias_ordenadas[:n_cercanas]
        
        # Crear string con IDs de las comunidades más cercanas
        ids_cercanas = [str(com['ID_Comunidad']) for com in n_mas_cercanas]
        ids_string = ', '.join(ids_cercanas)
        
        resultado = {
            'Item': granja['Item'],
            'CEs_Relacionadas': ids_string,
            'Granja_Departamento': granja['Departamento'],
            'Granja_Municipio': granja['Municipio'],
            'Granja_Latitud': lat_granja,
            'Granja_Longitud': lon_granja,
            'Comunidades_Cercanas': n_mas_cercanas
        }
        
        resultados.append(resultado)
        
        print(f"Granja {granja['Item']} ({granja['Municipio']}, {granja['Departamento']}):")
        print(f"  Comunidades más cercanas:")
        for i, com in enumerate(n_mas_cercanas[:5], 1):
            print(f"    {i}. ID {com['ID_Comunidad']}: {com['Nombre_Comunidad'][:50]}... "
                  f"({com['Distancia_km']:.2f} km)")
        print()
    
    return resultados

def crear_mapa_interactivo(granjas_df, comunidades_df, resultados):
    """
    Crea un mapa interactivo con Plotly mostrando granjas y comunidades.
    """
    fig = go.Figure()
    
    # Agregar granjas al mapa
    fig.add_trace(go.Scattermapbox(
        lat=granjas_df['Latitud'],
        lon=granjas_df['Longitud'],
        mode='markers',
        marker=dict(size=15, color='red', symbol='circle'),
        text=[f"Granja {row['Item']}<br>{row['Municipio']}, {row['Departamento']}<br>{row['Nombre del proyecto'][:100]}..." 
              for _, row in granjas_df.iterrows()],
        name='Granjas Solares',
        hovertemplate='<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
    ))
    
    # Agregar comunidades energéticas al mapa
    fig.add_trace(go.Scattermapbox(
        lat=comunidades_df['y'],
        lon=comunidades_df['x'],
        mode='markers',
        marker=dict(size=8, color='blue', symbol='circle'),
        text=[f"ID {row['ID']}: {row['Nombre de la comunidad']}<br>{row['Municipio']}, {row['Departamento']}<br>Potencia: {row['Potencia Estimada kWp']} kWp" 
              for _, row in comunidades_df.iterrows()],
        name='Comunidades Energéticas',
        hovertemplate='<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
    ))
    
    # Configurar el mapa
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=4.5, lon=-74),
            zoom=5
        ),
        title='Granjas Solares y Comunidades Energéticas en Colombia',
        height=700,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return fig

def crear_analisis_distancias(resultados):
    """
    Crea análisis estadísticos de las distancias.
    """
    distancias_todas = []
    distancias_por_granja = []
    
    for resultado in resultados:
        distancias_granja = [com['Distancia_km'] for com in resultado['Comunidades_Cercanas']]
        distancias_todas.extend(distancias_granja)
        distancias_por_granja.append({
            'Item': resultado['Item'],
            'Departamento': resultado['Granja_Departamento'],
            'Municipio': resultado['Granja_Municipio'],
            'Distancia_Min': min(distancias_granja),
            'Distancia_Media': np.mean(distancias_granja),
            'Distancia_Max': max(distancias_granja)
        })
    
    # Crear DataFrame con estadísticas por granja
    stats_df = pd.DataFrame(distancias_por_granja)
    
    # Crear gráfico de barras con distancias promedio
    fig_barras = px.bar(
        stats_df, 
        x='Item', 
        y='Distancia_Media',
        color='Departamento',
        title='Distancia Promedio a las 10 Comunidades Energéticas Más Cercanas por Granja',
        labels={'Distancia_Media': 'Distancia Promedio (km)', 'Item': 'Granja (Item)'},
        hover_data=['Municipio', 'Distancia_Min', 'Distancia_Max']
    )
    fig_barras.update_layout(height=500)
    
    # Crear histograma de todas las distancias
    fig_hist = px.histogram(
        x=distancias_todas,
        nbins=30,
        title='Distribución de Distancias entre Granjas y Comunidades Energéticas',
        labels={'x': 'Distancia (km)', 'y': 'Frecuencia'}
    )
    fig_hist.update_layout(height=400)
    
    return stats_df, fig_barras, fig_hist

def main():
    """
    Función principal que ejecuta todo el análisis.
    """
    print("=== ANÁLISIS DE PROXIMIDAD GRANJAS SOLARES - COMUNIDADES ENERGÉTICAS ===")
    print()
    
    # Cargar los datos
    print("1. Cargando datos...")
    try:
        # Cargar granjas
        granjas_df = pd.read_csv('Base granjas.csv')
        print(f"   Granjas cargadas: {len(granjas_df)}")
        
        # Cargar comunidades energéticas
        comunidades_df = pd.read_csv('Base comunidades energéticas.csv')
        print(f"   Comunidades energéticas cargadas: {len(comunidades_df)}")
        
    except Exception as e:
        print(f"   Error cargando datos: {e}")
        return
    
    # Verificar coordenadas válidas
    print("\n2. Verificando coordenadas...")
    granjas_validas = granjas_df.dropna(subset=['Latitud', 'Longitud'])
    comunidades_validas = comunidades_df.dropna(subset=['x', 'y'])
    print(f"   Granjas con coordenadas válidas: {len(granjas_validas)}")
    print(f"   Comunidades con coordenadas válidas: {len(comunidades_validas)}")
    
    # Encontrar comunidades cercanas
    print("\n3. Calculando proximidades...")
    resultados = encontrar_comunidades_cercanas(granjas_validas, comunidades_validas, 10)
    
    # Actualizar DataFrame de granjas con los resultados
    print("\n4. Actualizando base de datos de granjas...")
    for resultado in resultados:
        idx = granjas_df[granjas_df['Item'] == resultado['Item']].index[0]
        granjas_df.at[idx, 'CEs Relacionadas'] = resultado['CEs_Relacionadas']
    
    # Guardar la base actualizada
    granjas_df.to_csv('Base granjas_actualizada.csv', index=False)
    print("   Base de granjas actualizada guardada como 'Base granjas_actualizada.csv'")
    
    # Crear visualizaciones
    print("\n5. Generando visualizaciones...")
    
    # Mapa interactivo
    mapa_fig = crear_mapa_interactivo(granjas_validas, comunidades_validas, resultados)
    mapa_fig.write_html('mapa_granjas_comunidades.html')
    print("   Mapa interactivo guardado como 'mapa_granjas_comunidades.html'")
    
    # Análisis de distancias
    stats_df, fig_barras, fig_hist = crear_analisis_distancias(resultados)
    fig_barras.write_html('analisis_distancias_barras.html')
    fig_hist.write_html('distribucion_distancias.html')
    
    # Guardar estadísticas
    stats_df.to_csv('estadisticas_distancias.csv', index=False)
    print("   Análisis estadístico guardado como 'estadisticas_distancias.csv'")
    
    # Crear resumen detallado
    print("\n6. Generando resumen detallado...")
    resumen_detallado = []
    for resultado in resultados:
        for i, comunidad in enumerate(resultado['Comunidades_Cercanas'], 1):
            resumen_detallado.append({
                'Granja_Item': resultado['Item'],
                'Granja_Departamento': resultado['Granja_Departamento'],
                'Granja_Municipio': resultado['Granja_Municipio'],
                'Ranking': i,
                'Comunidad_ID': comunidad['ID_Comunidad'],
                'Comunidad_Nombre': comunidad['Nombre_Comunidad'],
                'Comunidad_Departamento': comunidad['Departamento_Comunidad'],
                'Comunidad_Municipio': comunidad['Municipio_Comunidad'],
                'Distancia_km': round(comunidad['Distancia_km'], 2),
                'Potencia_kWp': comunidad['Potencia_kWp'],
                'Inversion_Estimada': comunidad['Inversion_Estimada']
            })
    
    resumen_df = pd.DataFrame(resumen_detallado)
    resumen_df.to_csv('resumen_detallado_proximidades.csv', index=False)
    print("   Resumen detallado guardado como 'resumen_detallado_proximidades.csv'")
    
    # Mostrar resultados summary
    print("\n=== RESUMEN DE RESULTADOS ===")
    print(f"Total de granjas analizadas: {len(resultados)}")
    print(f"Total de comunidades disponibles: {len(comunidades_validas)}")
    print(f"\nDistancia promedio general: {np.mean([com['Distancia_km'] for resultado in resultados for com in resultado['Comunidades_Cercanas']]):.2f} km")
    print(f"Distancia mínima encontrada: {min([com['Distancia_km'] for resultado in resultados for com in resultado['Comunidades_Cercanas']]):.2f} km")
    print(f"Distancia máxima en top 10: {max([com['Distancia_km'] for resultado in resultados for com in resultado['Comunidades_Cercanas']]):.2f} km")
    
    print(f"\nArchivos generados:")
    print("- Base granjas_actualizada.csv (base original con CEs relacionadas)")
    print("- mapa_granjas_comunidades.html (mapa interactivo)")
    print("- analisis_distancias_barras.html (gráfico de barras)")
    print("- distribucion_distancias.html (histograma)")
    print("- estadisticas_distancias.csv (estadísticas por granja)")
    print("- resumen_detallado_proximidades.csv (todas las relaciones)")
    
    return granjas_df, resultados, stats_df

if __name__ == "__main__":
    granjas_actualizadas, resultados, estadisticas = main()
