"""
Configuración del Dashboard - Granjas Solares y Comunidades Energéticas
"""

# Configuración de Streamlit
PAGE_CONFIG = {
    "page_title": "Dashboard - Granjas Solares y Comunidades Energéticas",
    "page_icon": "☀️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Archivos de datos
DATA_FILES = {
    "granjas_actualizadas": "Base granjas_actualizada.csv",
    "granjas_original": "Base granjas.csv", 
    "comunidades": "Base comunidades energéticas.csv",
    "estadisticas": "estadisticas_distancias.csv",
    "resumen_detallado": "resumen_detallado_proximidades.csv"
}

# Configuración de colores y tema
THEME_COLORS = {
    "primary": "#FF6B35",
    "secondary": "#FFD23F", 
    "accent": "#F18F01",
    "success": "#00D9FF",
    "danger": "#FF3366",
    "bg_dark": "#0A0A0A",
    "bg_card": "#1A1A1A",
    "bg_light": "#2A2A2A",
    "text_primary": "#FFFFFF",
    "text_secondary": "#E5E5E5",
    "text_muted": "#B0B0B0",
    "border": "#333333"
}

# Opciones de navegación
NAVIGATION_OPTIONS = [
    "🔍 Explorar por Granja",
    "🗺️ Mapas Interactivos", 
    "📈 Estadísticas Detalladas",
    "📋 Datos y Tablas"
]

# Configuración de mapas
MAP_CONFIG = {
    "center_colombia": [4.5, -74],
    "zoom_start": 6,
    "comunidades_sample_size": 500,
    "folium_sample_size": 100
}
