#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cargar indicadores directamente leyendo el archivo indicators.py
sin necesidad de importar los módulos del backend
"""

import os
import sys
import re
from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "https://aoykpiievtadhwssugvs.supabase.co")
SUPABASE_ANON_KEY = os.getenv("VITE_SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Mapeo de dimensiones y subdimensiones según el backend
DIMENSION_MAP = {
    "EMPRENDIMIENTO_E_INNOVACION": "Emprendimiento e innovación",
    "CAPITAL_HUMANO": "Capital humano",
    "ECOSISTEMA_Y_COLABORACION": "Ecosistema y colaboración",
    "INFRAESTRUCTURA_DIGITAL": "Infraestructura digital",
    "SERVICIOS_PUBLICOS_DIGITALES": "Servicios públicos digitales",
    "SOSTENIBILIDAD_DIGITAL": "Sostenibilidad digital",
    "TRANSFORMACION_DIGITAL": "Transformación digital empresarial",
}

SUBDIMENSION_MAP = {
    "ACCESO_FINANCIACION": "Acceso a financiación",
    "DINAMISMO_EMPRENDEDOR": "Dinamismo emprendedor",
    "INFRAESTRUCTURA_APOYO": "Infraestructura de apoyo",
    "POLITICAS_FOMENTO": "Políticas de fomento",
    "COMPETENCIAS_DIGITALES": "Competencias digitales",
    "FORMACION_CONTINUA": "Formación continua",
    "TALENTO_PROFESIONAL": "Talento profesional",
    "ATRACTIVO_ECOSISTEMA": "Atractivo del ecosistema",
    "PROVISION_TECNOLOGICA": "Provision tecnológica",
    "TRANSFERENCIA_CONOCIMIENTO": "Transferencia de conocimiento",
    "ACCESO_INFRAESTRUCTURAS": "Acceso a infraestructuras",
    "DISPONIBILIDAD_SERVICIOS_DIGITALES": "Disponibilidad de servicios digitales",
    "INTEGRACION_ADMINISTRACION": "Integración con administración",
    "ECONOMIA_CIRCULAR": "Economía circular",
    "HUELLA_AMBIENTAL": "Huella ambiental",
    "ORGANIZACION_DIGITAL": "Organización digital",
    "DIGITALIZACION_BASICA": "Digitalización básica",
    "E_COMMERCE": "E-commerce",
    "TECNOLOGIAS_AVANZADAS": "Tecnologías avanzadas",
}


def parse_indicators_file(file_path):
    """Parsea el archivo indicators.py y extrae los indicadores"""
    indicadores = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar patrones de Indicador(...)
        pattern = r'"([^"]+)":\s*Indicador\([^)]+\)'
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            nombre = match.group(1)
            
            # Extraer atributos del indicador
            indicador_block = match.group(0)
            
            # Buscar dimension
            dim_match = re.search(r'dimension=Dimension\.(\w+)', indicador_block)
            dimension = dim_match.group(1) if dim_match else None
            
            # Buscar subdimension
            subdim_match = re.search(r'subdimension=Subdimension\.(\w+)', indicador_block)
            subdimension = subdim_match.group(1) if subdim_match else None
            
            # Buscar otros campos
            origen_match = re.search(r'origen\s*=\s*"([^"]*)"', indicador_block)
            origen = origen_match.group(1) if origen_match else ''
            
            importancia_match = re.search(r'importancia\s*=\s*"([^"]*)"', indicador_block)
            importancia = importancia_match.group(1) if importancia_match else 'Media'
            
            fuente_match = re.search(r'fuente\s*=\s*"([^"]*)"', indicador_block)
            fuente = fuente_match.group(1) if fuente_match else ''
            
            if dimension and subdimension:
                dimension_nombre = DIMENSION_MAP.get(dimension, dimension)
                subdimension_nombre = SUBDIMENSION_MAP.get(subdimension, subdimension)
                
                indicadores.append({
                    "nombre": nombre,
                    "nombre_subdimension": subdimension_nombre,
                    "importancia": importancia[:30] if importancia else "Media",  # VARCHAR(30)
                    "formula": "",  # VARCHAR(50) - se puede extraer de formula_calculo si es necesario
                    "fuente": fuente[:50] if fuente else "",  # VARCHAR(50)
                    "origen_indicador": origen[:30] if origen else ""  # VARCHAR(30)
                })
        
        return indicadores
    
    except Exception as e:
        print(f"❌ Error parseando archivo: {e}")
        return []


def load_indicadores():
    """Carga los indicadores en Supabase"""
    print("📊 Cargando indicadores...")
    
    indicators_file = "/Users/chaumesanchez/Downloads/Camara_de_comercio/data/processed/indicadores/indicators.py"
    
    if not os.path.exists(indicators_file):
        print(f"❌ Archivo no encontrado: {indicators_file}")
        return []
    
    indicadores = parse_indicators_file(indicators_file)
    
    if not indicadores:
        print("⚠️  No se pudieron extraer indicadores del archivo")
        return []
    
    print(f"   📋 Encontrados {len(indicadores)} indicadores")
    
    try:
        # Insertar en lotes de 100
        batch_size = 100
        total_inserted = 0
        
        for i in range(0, len(indicadores), batch_size):
            batch = indicadores[i:i + batch_size]
            result = supabase.table("definicion_indicadores").upsert(batch, on_conflict="nombre").execute()
            total_inserted += len(batch)
            print(f"   ✅ Lote {i//batch_size + 1}: {len(batch)} indicadores")
        
        print(f"✅ {total_inserted} indicadores cargados en total")
        return indicadores
    
    except Exception as e:
        print(f"❌ Error cargando indicadores: {e}")
        raise


def main():
    """Función principal"""
    print("🚀 Iniciando carga de indicadores en Supabase...\n")
    
    try:
        load_indicadores()
        print("\n✅ Carga de indicadores completada")
        
    except Exception as e:
        print(f"\n❌ Error durante la carga: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

