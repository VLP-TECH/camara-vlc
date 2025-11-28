#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script completo para cargar todos los datos de Brainnova a Supabase
Ejecutar desde el directorio raíz del proyecto frontend
"""

import os
import sys
from pathlib import Path
import json
import pandas as pd
from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = "https://aoykpiievtadhwssugvs.supabase.co"
SUPABASE_SERVICE_KEY = os.getenv("VITE_SUPABASE_SERVICE_ROLE_KEY", "")

if not SUPABASE_SERVICE_KEY:
    # Usar anon key como fallback
    SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY"
    print("⚠️  Usando ANON KEY. Si tienes problemas de permisos, configura VITE_SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Rutas
BACKEND_DIR = Path("/Users/chaumesanchez/Downloads/Camara_de_comercio")
DATA_DIR = BACKEND_DIR / "data" / "processed"

# Estructura de dimensiones y subdimensiones
DIMENSIONES = {
    "Emprendimiento e Innovación": {
        "peso": 10,
        "subdimensiones": [
            "Acceso a Financiación",
            "Dinamismo Emprendedor",
            "Infraestructura de Apoyo",
            "Políticas de Fomento"
        ]
    },
    "Capital Humano": {
        "peso": 20,
        "subdimensiones": [
            "Competencias Digitales",
            "Formación Continua",
            "Talento Profesional"
        ]
    },
    "Ecosistema y Colaboración": {
        "peso": 15,
        "subdimensiones": [
            "Atractivo del Ecosistema",
            "Provisión Tecnológica",
            "Transferencia de Conocimiento"
        ]
    },
    "Infraestructura Digital": {
        "peso": 15,
        "subdimensiones": [
            "Acceso a Infraestructuras"
        ]
    },
    "Servicios Públicos Digitales": {
        "peso": 10,
        "subdimensiones": [
            "Disponibilidad de Servicios Digitales",
            "Integración con Administración"
        ]
    },
    "Sostenibilidad Digital": {
        "peso": 5,
        "subdimensiones": [
            "Economía Circular",
            "Huella Ambiental"
        ]
    },
    "Transformación Digital": {
        "peso": 30,
        "subdimensiones": [
            "Organización Digital",
            "Digitalización Básica",
            "E-Commerce",
            "Tecnologías Avanzadas"
        ]
    }
}

def clear_all_tables():
    """Limpia todas las tablas de Supabase"""
    print("\n🧹 Limpiando tablas existentes...")
    
    tables = [
        'resultado_indicadores',
        'definicion_indicadores',
        'subdimensiones',
        'dimensiones'
    ]
    
    for table in tables:
        try:
            # Usar delete sin filtro para limpiar toda la tabla
            supabase.table(table).delete().gte('created_at', '1900-01-01').execute()
            print(f"  ✓ {table} limpiada")
        except Exception as e:
            print(f"  ⚠️  Error limpiando {table}: {e}")

def load_dimensiones():
    """Carga las dimensiones en Supabase"""
    print("\n📊 Cargando dimensiones...")
    
    for nombre, info in DIMENSIONES.items():
        try:
            data = {
                'nombre': nombre,
                'peso': info['peso']
            }
            result = supabase.table('dimensiones').insert(data).execute()
            print(f"  ✓ {nombre} (peso: {info['peso']})")
        except Exception as e:
            print(f"  ❌ Error con {nombre}: {e}")

def load_subdimensiones():
    """Carga las subdimensiones en Supabase"""
    print("\n📋 Cargando subdimensiones...")
    
    for dim_nombre, info in DIMENSIONES.items():
        for subdim_nombre in info['subdimensiones']:
            try:
                data = {
                    'nombre': subdim_nombre,
                    'nombre_dimension': dim_nombre,
                    'peso': 0  # Peso predeterminado
                }
                result = supabase.table('subdimensiones').insert(data).execute()
                print(f"  ✓ {subdim_nombre} → {dim_nombre}")
            except Exception as e:
                if 'duplicate key' not in str(e).lower():
                    print(f"  ❌ Error con {subdim_nombre}: {e}")

def load_indicadores_from_csv():
    """Carga indicadores desde archivos CSV de resultados"""
    print("\n📈 Cargando indicadores desde CSVs...")
    
    # Directorios con CSVs de resultados
    result_dirs = [
        DATA_DIR / "eurostat" / "filtered" / "resultado",
        DATA_DIR / "ine" / "filtered" / "resultado",
        DATA_DIR / "digital_decade" / "filtered" / "resultado",
    ]
    
    indicadores_procesados = set()
    total_resultados = 0
    
    for result_dir in result_dirs:
        if not result_dir.exists():
            continue
            
        for csv_file in result_dir.glob("*.csv"):
            try:
                nombre_indicador = csv_file.stem.replace('_', ' ').title()
                
                # Solo procesar cada indicador una vez
                if nombre_indicador in indicadores_procesados:
                    continue
                    
                # Leer CSV
                df = pd.read_csv(csv_file)
                
                # Determinar subdimensión basándose en el nombre
                subdimension = determinar_subdimension(nombre_indicador)
                
                # Insertar definición de indicador si no existe
                try:
                    indicador_data = {
                        'nombre': nombre_indicador,
                        'formula': 'Dato crudo',
                        'origen_indicador': determinar_origen(csv_file.parent.parent.parent.name),
                        'nombre_subdimension': subdimension,
                        'importancia': 'Media',
                        'unidad': determinar_unidad(nombre_indicador)
                    }
                    supabase.table('definicion_indicadores').insert(indicador_data).execute()
                    print(f"  ✓ Definición: {nombre_indicador}")
                except Exception as e:
                    if 'duplicate key' not in str(e).lower():
                        print(f"  ⚠️  Error definición {nombre_indicador}: {e}")
                
                # Insertar resultados
                resultados_batch = []
                for _, row in df.iterrows():
                    try:
                        resultado = {
                            'nombre_indicador': nombre_indicador,
                            'valor_calculado': float(row.get('valor', row.get('Valor', 0))),
                            'pais': str(row.get('pais', row.get('Pais', row.get('geo', 'España')))),
                            'periodo': int(row.get('periodo', row.get('año', row.get('time', 2024)))),
                            'provincia': str(row.get('provincia', None)) if 'provincia' in row else None,
                            'sector': str(row.get('sector', None)) if 'sector' in row else None,
                            'tamano_empresa': str(row.get('tamano_empresa', row.get('tamaño', None))) if 'tamano_empresa' in row or 'tamaño' in row else None
                        }
                        resultados_batch.append(resultado)
                        
                        # Insertar en lotes de 100
                        if len(resultados_batch) >= 100:
                            supabase.table('resultado_indicadores').insert(resultados_batch).execute()
                            total_resultados += len(resultados_batch)
                            resultados_batch = []
                            
                    except Exception as e:
                        print(f"  ⚠️  Error fila: {e}")
                
                # Insertar batch final
                if resultados_batch:
                    supabase.table('resultado_indicadores').insert(resultados_batch).execute()
                    total_resultados += len(resultados_batch)
                
                indicadores_procesados.add(nombre_indicador)
                print(f"  ✓ Resultados cargados: {nombre_indicador} ({len(df)} filas)")
                
            except Exception as e:
                print(f"  ❌ Error procesando {csv_file.name}: {e}")
    
    print(f"\n✅ Total indicadores procesados: {len(indicadores_procesados)}")
    print(f"✅ Total resultados cargados: {total_resultados}")

def determinar_subdimension(nombre_indicador):
    """Determina la subdimensión basándose en el nombre del indicador"""
    nombre_lower = nombre_indicador.lower()
    
    if any(word in nombre_lower for word in ['big data', 'ia', 'inteligencia artificial', 'crm', 'erp']):
        return 'Tecnologías Avanzadas'
    elif any(word in nombre_lower for word in ['venta online', 'e-commerce', 'comercio electrónico']):
        return 'E-Commerce'
    elif any(word in nombre_lower for word in ['web', 'presencia', 'redes sociales']):
        return 'Digitalización Básica'
    elif any(word in nombre_lower for word in ['formacion', 'formación', 'habilidades']):
        return 'Formación Continua'
    elif any(word in nombre_lower for word in ['cobertura', 'banda ancha', 'fibra', 'conectividad']):
        return 'Acceso a Infraestructuras'
    elif any(word in nombre_lower for word in ['banca electronica', 'e-gobierno', 'autoridades públicas']):
        return 'Disponibilidad de Servicios Digitales'
    elif any(word in nombre_lower for word in ['teletrabajo', 'cloud', 'nube']):
        return 'Organización Digital'
    else:
        return 'Digitalización Básica'  # Por defecto

def determinar_origen(directorio):
    """Determina el origen del indicador basándose en el directorio"""
    if 'eurostat' in directorio:
        return 'Eurostat'
    elif 'ine' in directorio:
        return 'INE'
    elif 'digital_decade' in directorio or 'digital-strategy' in directorio:
        return 'Digital Decade'
    elif 'cnmc' in directorio:
        return 'CNMC'
    elif 'worldbank' in directorio.lower():
        return 'World Bank'
    else:
        return 'Otro'

def determinar_unidad(nombre_indicador):
    """Determina la unidad basándose en el nombre del indicador"""
    nombre_lower = nombre_indicador.lower()
    
    if any(word in nombre_lower for word in ['porcentaje', '%', 'tasa', 'proporción']):
        return '%'
    elif any(word in nombre_lower for word in ['personas', 'empresas', 'usuarios', 'número']):
        return 'unidades'
    elif any(word in nombre_lower for word in ['precio', 'coste', 'gasto', 'ingreso']):
        return '€'
    elif any(word in nombre_lower for word in ['velocidad', 'mbps']):
        return 'Mbps'
    else:
        return 'unidades'

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 CARGA COMPLETA DE DATOS BRAINNOVA A SUPABASE")
    print("=" * 60)
    
    try:
        # 1. Limpiar tablas
        clear_all_tables()
        
        # 2. Cargar dimensiones
        load_dimensiones()
        
        # 3. Cargar subdimensiones
        load_subdimensiones()
        
        # 4. Cargar indicadores y resultados
        load_indicadores_from_csv()
        
        print("\n" + "=" * 60)
        print("✅ CARGA COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        
        # Mostrar resumen
        print("\n📊 RESUMEN:")
        for table in ['dimensiones', 'subdimensiones', 'definicion_indicadores', 'resultado_indicadores']:
            try:
                count_result = supabase.table(table).select('*', count='exact').execute()
                count = len(count_result.data) if count_result.data else 0
                print(f"  • {table}: {count} registros")
            except Exception as e:
                print(f"  • {table}: Error contando - {e}")
        
    except Exception as e:
        print(f"\n❌ Error durante la carga: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

