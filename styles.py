"""
Estilos CSS para el Dashboard
"""

def get_custom_css():
    """Retorna el CSS personalizado para el dashboard"""
    return """
<style>
    /* Fuentes optimizadas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #FF6B35;
        --secondary-color: #FFD23F;
        --accent-color: #F18F01;
        --success-color: #00D9FF;
        --danger-color: #FF3366;
        --bg-dark: #0A0A0A;
        --bg-card: #1A1A1A;
        --bg-light: #2A2A2A;
        --text-primary: #FFFFFF;
        --text-secondary: #E5E5E5;
        --text-muted: #B0B0B0;
        --border: #333333;
        --shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Base */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg-dark);
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* Contenedor principal */
    .main .block-container {
        background: var(--bg-dark);
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Títulos */
    h1, .main h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 1rem;
        text-align: center;
        letter-spacing: -0.02em;
    }
    
    h2, .main h2 {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 500;
        color: var(--text-primary);
        margin: 2rem 0 1rem 0;
        letter-spacing: -0.01em;
    }
    
    h3, .main h3 {
        font-family: 'Poppins', sans-serif;
        font-size: 1.4rem;
        font-weight: 500;
        color: var(--accent-color);
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Texto */
    p, .stMarkdown p, .stText {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.7;
        color: var(--text-secondary);
    }
    
    /* Header principal */
    .main-header {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, #1A1A1A 0%, #0A0A0A 100%) !important;
    }
    
    .stSidebar > div {
        background: linear-gradient(180deg, #1A1A1A 0%, #0A0A0A 100%) !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #1A1A1A 0%, #0A0A0A 100%) !important;
        border-right: 3px solid var(--primary-color) !important;
        box-shadow: 2px 0 10px rgba(255, 107, 53, 0.1) !important;
    }
    
    /* Cards */
    .content-card {
        background: var(--bg-card);
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .content-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
    }
    
    /* Botones */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: var(--accent-color);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
    }
    
    /* DataFrames */
    .stDataFrame {
        font-family: 'Inter', sans-serif;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    /* Métricas */
    [data-testid="metric-container"] {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--bg-light);
        border: 1px solid var(--border);
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-color);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid var(--border);
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-muted);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.8rem 1.5rem;
        border-radius: 6px;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
        font-weight: 600;
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 8px;
        border: none;
        padding: 1rem;
        font-family: 'Inter', sans-serif;
        margin: 1rem 0;
    }
    
    .stInfo {
        background: rgba(0, 217, 255, 0.1);
        color: var(--success-color);
        border-left: 4px solid var(--success-color);
    }
    
    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-color);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1, .main h1 { font-size: 1.8rem; }
        h2, .main h2 { font-size: 1.4rem; }
        .content-card { padding: 1rem; }
        .main-header { padding: 1.5rem 1rem; }
    }
</style>
"""
