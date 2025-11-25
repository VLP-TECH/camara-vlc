#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cargar datos de Brainnova desde el backend a Supabase
Ejecuta este script desde el directorio del backend
"""

import os
import sys
from pathlib import Path
from supabase import create_client, Client
import json

# Añadir el directorio del backend al path
backend_dir = Path(__file__).parent.parent / "Camara_de_comercio"
if not backend_dir.exists():
    backend_dir = Path("/Users/chaumesanchez/Downloads/Camara_de_comercio")

sys.path.insert(0, str(backend_dir))

# Configuración de Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "https://aoykpiievtadhwssugvs.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("VITE_SUPABASE_SERVICE_ROLE_KEY", "")

if not SUPABASE_SERVICE_KEY:
    # Usar anon key como fallback (funcionará si las políticas de inserción están habilitadas)
    SUPABASE_SERVICE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Importar módulos del backend
try:
    from database.setup import DATOS_ESG, fusionar_datos
    from data.processed.indicadores.indicators import CATALOGO_COMPLETO
    from data.processed.indicadores.roles import CATALOGO_ROLES
    from modelos.models import Dimension, Subdimension
except ImportError as e:
    print(f"❌ Error importando módulos del backend: {e}")
    print(f"   Asegúrate de ejecutar este script desde el directorio del backend")
    sys.exit(1)


def load_dimensiones():
    """Carga las dimensiones en Supabase"""
    print("📊 Cargando dimensiones...")
    
    dimensiones = []
    for nombre_dim, datos_dim in DATOS_ESG.items():
        dimensiones.append({
            "nombre": nombre_dim,
            "peso": datos_dim['peso']
        })
    
    result = supabase.table("dimensiones").upsert(dimensiones, on_conflict="nombre").execute()
    print(f"✅ {len(dimensiones)} dimensiones cargadas")
    return result


def load_subdimensiones():
    """Carga las subdimensiones en Supabase"""
    print("📊 Cargando subdimensiones...")
    
    subdimensiones = []
    for nombre_dim, datos_dim in DATOS_ESG.items():
        for datos_sub in datos_dim['subdimensiones']:
            subdimensiones.append({
                "nombre": datos_sub['nombre'],
                "nombre_dimension": nombre_dim,
                "peso": datos_sub['peso']
            })
    
    result = supabase.table("subdimensiones").upsert(subdimensiones, on_conflict="nombre").execute()
    print(f"✅ {len(subdimensiones)} subdimensiones cargadas")
    return result


def load_indicadores():
    """Carga los indicadores en Supabase"""
    print("📊 Cargando indicadores...")
    
    lista_indicadores = fusionar_datos()
    indicadores = []
    
    for indicador in lista_indicadores:
        # Buscar la subdimensión correspondiente
        nombre_subdimension = indicador['subdimension']
        
        indicadores.append({
            "nombre": indicador['nombre'],
            "nombre_subdimension": nombre_subdimension,
            "importancia": indicador.get('importancia', 'Media'),
            "formula": indicador.get('formula', ''),
            "fuente": indicador.get('fuente', ''),
            "origen_indicador": indicador.get('origen', '')
        })
    
    result = supabase.table("definicion_indicadores").upsert(indicadores, on_conflict="nombre").execute()
    print(f"✅ {len(indicadores)} indicadores cargados")
    return result


def load_componentes():
    """Carga los componentes de indicadores en Supabase"""
    print("📊 Cargando componentes de indicadores...")
    
    componentes = []
    
    for rol_info in CATALOGO_ROLES:
        nombre_indicador = rol_info['nombre_indicador']
        
        for datos_comp in rol_info.get('componentes', []):
            descripcion_dato = datos_comp.get('descripcion_dato', '')
            if descripcion_dato and descripcion_dato != 'nan':
                componentes.append({
                    "nombre_indicador": nombre_indicador,
                    "descripcion_dato": descripcion_dato,
                    "fuente_tabla": datos_comp.get('fuente_tabla', 'DATOS_CRUDOS')
                })
    
    if componentes:
        # Insertar en lotes de 1000
        batch_size = 1000
        for i in range(0, len(componentes), batch_size):
            batch = componentes[i:i + batch_size]
            result = supabase.table("componentes_indicador").insert(batch).execute()
        
        print(f"✅ {len(componentes)} componentes cargados")
    else:
        print("⚠️  No se encontraron componentes para cargar")
    
    return componentes


def main():
    """Función principal"""
    print("🚀 Iniciando carga de datos en Supabase...\n")
    
    try:
        # 1. Cargar dimensiones
        load_dimensiones()
        print()
        
        # 2. Cargar subdimensiones
        load_subdimensiones()
        print()
        
        # 3. Cargar indicadores
        load_indicadores()
        print()
        
        # 4. Cargar componentes
        load_componentes()
        print()
        
        print("✅ Carga de datos completada")
        print("\n📝 Próximos pasos:")
        print("   - Los datos crudos y macro deben cargarse desde los CSV procesados")
        print("   - Usa el endpoint de ingesta del backend para cargar datos históricos")
        
    except Exception as e:
        print(f"\n❌ Error durante la carga: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

