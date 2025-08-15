#!/usr/bin/env python3
"""
Launcher para el Dashboard Limpio - Granjas Solares y Comunidades Energéticas
"""

import subprocess
import sys
import os

def main():
    print("🚀 Iniciando Dashboard Limpio - Granjas Solares y Comunidades Energéticas...")
    print("📁 Directorio de trabajo:", os.getcwd())
    print("🔧 Configuración: Auto-reload habilitado")
    print("🌐 URL: http://localhost:8503")
    print("=" * 60)
    
    try:
        # Ejecutar Streamlit con configuración optimizada
        subprocess.run([
            "streamlit", "run", "dashboard_estable.py",
            "--server.port=8503",
            "--server.runOnSave=true",
            "--server.allowRunOnSave=true",
            "--browser.gatherUsageStats=false",
            "--server.headless=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⚡ Dashboard detenido por el usuario")
    except FileNotFoundError:
        print("❌ Error: Streamlit no está instalado")
        print("💡 Instala con: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al iniciar dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
