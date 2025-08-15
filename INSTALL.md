# 🚀 Instalación y Configuración

## Requisitos del Sistema
- Python 3.8 o superior
- Git (para clonar el repositorio)

## Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/MelissaCardona2003/coordenadas.git
cd coordenadas
```

### 2. Crear Entorno Virtual
```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar Dashboard
```bash
# Dashboard principal estable
streamlit run dashboard_estable.py

# O usar el lanzador
python lanzar_dashboard_limpio.py
```

### 5. Acceder al Dashboard
Abrir en navegador: `http://localhost:8501` o `http://localhost:8504`

## 📊 Archivos Principales

### Scripts de Análisis
- `analisis_proximidad_simple.py` - Análisis principal de proximidad
- `dashboard_estable.py` - Dashboard web interactivo optimizado

### Datos de Entrada
- `Base granjas.csv` - 15 granjas solares
- `Base comunidades energéticas.csv` - 17,518 comunidades energéticas

### Resultados Generados
- `Base granjas_actualizada.csv` - Granjas con CEs relacionadas
- `estadisticas_distancias.csv` - Estadísticas por granja
- `resumen_detallado_proximidades.csv` - 150 relaciones detalladas

### Estructura Modular
- `config_original.py` - Configuraciones del sistema
- `data_loader.py` - Carga de datos
- `charts_original.py` - Gráficos y visualizaciones
- `components.py` - Componentes UI
- `styles.py` - Estilos CSS
- `views.py` - Vistas del dashboard

## 🔧 Troubleshooting

### Problema: Error de importación
```bash
pip install --upgrade streamlit pandas numpy plotly folium
```

### Problema: Puerto ocupado
```bash
streamlit run dashboard_estable.py --server.port=8505
```

### Problema: Datos faltantes
Verificar que todos los archivos CSV estén en el directorio raíz.

## 📞 Soporte
Proyecto desarrollado para el Ministerio de Minas y Energías - Colombia
