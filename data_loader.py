"""
Módulo para cargar y procesar datos
"""
import pandas as pd
import streamlit as st
from io import BytesIO
from config import DATA_FILES

@st.cache_data
def cargar_datos():
    """Cargar todos los datasets necesarios"""
    try:
        datasets = {}
        for key, filename in DATA_FILES.items():
            datasets[key] = pd.read_csv(filename)
        
        return (
            datasets["granjas_actualizadas"],
            datasets["granjas_original"], 
            datasets["comunidades"],
            datasets["estadisticas"],
            datasets["resumen_detallado"]
        )
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None, None, None

def to_excel(df):
    """Convertir DataFrame a Excel y retornar bytes"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    return output.getvalue()

def crear_tabla_principal(granjas_actualizadas, estadisticas):
    """Crear tabla principal con todos los datos"""
    tabla_principal = []
    
    for _, granja in granjas_actualizadas.iterrows():
        item = granja['Item']
        ces_ids = granja['CEs Relacionadas']
        stats_granja = estadisticas[estadisticas['Item'] == item].iloc[0]
        
        tabla_principal.append({
            'Granja': f"Granja {item}",
            'Ubicación': f"{granja['Municipio']}, {granja['Departamento']}",
            'Potencia_kW': granja['Potencia  KW'],
            'IDs_10_CEs_Mas_Cercanas': ces_ids,
            'Distancia_Promedio_km': round(stats_granja['Distancia_Media'], 2),
            'Distancia_Minima_km': round(stats_granja['Distancia_Min'], 2),
            'Beneficiarios': granja['Beneficiarios']
        })
    
    return pd.DataFrame(tabla_principal)
