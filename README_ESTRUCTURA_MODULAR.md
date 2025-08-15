# Dashboard Granjas Solares - Estructura Modular

## 📁 Arquitectura del Proyecto

### Archivos Principales

#### 🎛️ `dashboard_limpio.py`
- **Función**: Archivo principal del dashboard
- **Contenido**: Orquesta toda la aplicación, importa módulos
- **Responsabilidades**: 
  - Configuración de Streamlit
  - Control de navegación principal
  - Coordinación entre módulos

#### ⚙️ `config.py`
- **Función**: Configuración centralizada
- **Contenido**:
  - Configuración de página Streamlit
  - Rutas de archivos de datos
  - Colores y tema
  - Opciones de navegación
  - Configuración de mapas

#### 🎨 `styles.py`
- **Función**: Estilos CSS del dashboard
- **Contenido**:
  - CSS personalizado optimizado
  - Variables de colores
  - Tipografía (Inter, Poppins)
  - Responsive design
  - Animaciones simples

#### 💾 `data_loader.py`
- **Función**: Carga y procesamiento de datos
- **Contenido**:
  - Función `cargar_datos()` con cache
  - Conversión a Excel (`to_excel()`)
  - Creación de tabla principal
  - Manejo de errores de datos

#### 📊 `charts.py`
- **Función**: Gráficos y visualizaciones
- **Contenido**:
  - Gráfico de barras de distancias
  - Histograma de distribución
  - Mapas con Folium
  - Mapas scatter con Plotly

#### 🧩 `components.py`
- **Función**: Componentes reutilizables de UI
- **Contenido**:
  - Header principal
  - Métricas del sidebar
  - Métricas principales
  - Información de granjas
  - Botones de descarga
  - Footer

#### 📱 `views.py`
- **Función**: Vistas completas del dashboard
- **Contenido**:
  - Vista explorar por granja
  - Vista mapas interactivos
  - Vista estadísticas detalladas
  - Vista datos y tablas

### 🚀 Scripts de Lanzamiento

#### `lanzar_dashboard_limpio.py`
- Script ejecutable para iniciar el dashboard
- Configuración automática de parámetros
- Manejo de errores
- Puerto: 8503

## 🏗️ Ventajas de la Estructura Modular

### ✅ Mantenibilidad
- Código organizado por responsabilidades
- Fácil localización de funcionalidades
- Modificaciones aisladas por módulo

### ✅ Escalabilidad  
- Fácil agregar nuevas vistas
- Componentes reutilizables
- Configuración centralizada

### ✅ Legibilidad
- Archivos pequeños y enfocados
- Nombres descriptivos
- Separación clara de concerns

### ✅ Testing
- Módulos testeable independientemente
- Funciones puras donde es posible
- Dependencias claras

### ✅ Performance
- Carga condicional de módulos
- Cache optimizado
- CSS limpio sin efectos pesados

## 🔧 Uso

### Iniciar Dashboard
```bash
# Opción 1: Script automático
python lanzar_dashboard_limpio.py

# Opción 2: Streamlit directo
source .venv/bin/activate
streamlit run dashboard_limpio.py --server.port=8503
```

### Modificar Configuración
- Editar `config.py` para cambios de configuración
- Editar `styles.py` para cambios visuales
- El dashboard se recarga automáticamente

### Agregar Nueva Vista
1. Crear función en `views.py`
2. Agregar opción en `config.NAVIGATION_OPTIONS`
3. Agregar caso en `dashboard_limpio.py`

## 📊 Datos Procesados
- **15 granjas solares** con coordenadas y especificaciones
- **17,518 comunidades energéticas** con ubicaciones
- **Algoritmo**: Cálculos geodésicos precisos
- **Resultado**: 10 CEs más cercanas por granja

---
**Desarrollado para el Ministerio de Minas y Energías - Colombia**
