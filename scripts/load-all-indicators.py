#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cargar TODOS los indicadores disponibles a Supabase
Incluye indicadores desde CSVs y desde el catálogo de indicadores
"""

import os
from pathlib import Path
import pandas as pd
from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = "https://aoykpiievtadhwssugvs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Rutas
BACKEND_DIR = Path("/Users/chaumesanchez/Downloads/Camara_de_comercio")
DATA_DIR = BACKEND_DIR / "data" / "processed"
INDICADORES_DIR = DATA_DIR / "indicadores"

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
    elif any(word in nombre_lower for word in ['cobertura', 'banda ancha', 'fibra', 'conectividad', 'vhcn']):
        return 'Acceso a Infraestructuras'
    elif any(word in nombre_lower for word in ['banca electronica', 'e-gobierno', 'autoridades públicas', 'interaccion']):
        return 'Disponibilidad de Servicios Digitales'
    elif any(word in nombre_lower for word in ['teletrabajo', 'cloud', 'nube', 'computing']):
        return 'Organización Digital'
    elif any(word in nombre_lower for word in ['i+d', 'investigacion', 'desarrollo']):
        return 'Tecnologías Avanzadas'
    else:
        return 'Digitalización Básica'

def determinar_origen(directorio):
    """Determina el origen del indicador"""
    if 'eurostat' in str(directorio):
        return 'Eurostat'
    elif 'ine' in str(directorio):
        return 'INE'
    elif 'digital_decade' in str(directorio) or 'digital-strategy' in str(directorio):
        return 'Digital Decade'
    elif 'cnmc' in str(directorio):
        return 'CNMC'
    elif 'worldbank' in str(directorio).lower():
        return 'World Bank'
    else:
        return 'Otro'

def load_indicadores_from_csv():
    """Carga TODOS los indicadores desde archivos CSV"""
    print("\n📈 Cargando indicadores desde CSVs...")
    
    # Buscar en todos los directorios de resultado
    result_dirs = [
        DATA_DIR / "eurostat" / "filtered" / "resultado",
        DATA_DIR / "ine" / "filtered" / "resultado",
        DATA_DIR / "digital_decade" / "filtered" / "resultado",
        DATA_DIR / "cnmc" / "filtered" / "resultado",
    ]
    
    total_indicadores = 0
    total_resultados = 0
    indicadores_procesados = set()
    
    for result_dir in result_dirs:
        if not result_dir.exists():
            continue
            
        print(f"\n  📁 Procesando: {result_dir.name}")
        
        for csv_file in result_dir.glob("*.csv"):
            try:
                # Mejorar el nombre del indicador
                # Mejorar el nombre del indicador
                nombre_indicador = csv_file.stem.replace('_', ' ').title()
                # Corregir nombres comunes
                nombre_indicador = nombre_indicador.replace('Ia', 'IA')
                nombre_indicador = nombre_indicador.replace('Tic', 'TIC')
                nombre_indicador = nombre_indicador.replace('Crm', 'CRM')
                nombre_indicador = nombre_indicador.replace('Erp', 'ERP')
                nombre_indicador = nombre_indicador.replace('Vhcn', 'VHCN')
                nombre_indicador = nombre_indicador.replace('I+D', 'I+D')
                
                # Procesar todos los archivos, incluso si ya existe la definición
                # (para asegurar que todos los resultados se carguen)
                
                # Leer CSV
                df = pd.read_csv(csv_file)
                
                if len(df) == 0:
                    continue
                
                # Insertar definición (upsert: insertar o actualizar)
                try:
                    indicador_data = {
                        'nombre': nombre_indicador,
                        'formula': 'Dato crudo',
                        'origen_indicador': determinar_origen(result_dir),
                        'nombre_subdimension': determinar_subdimension(nombre_indicador),
                        'importancia': 'Media'
                    }
                    # Intentar insertar, si falla por duplicado, actualizar
                    try:
                        supabase.table('definicion_indicadores').insert(indicador_data).execute()
                        total_indicadores += 1
                        print(f"    ✓ {nombre_indicador} (nuevo)")
                    except Exception as insert_error:
                        if 'duplicate key' in str(insert_error).lower() or 'unique constraint' in str(insert_error).lower():
                            # Ya existe, actualizar
                            supabase.table('definicion_indicadores').update(indicador_data).eq('nombre', nombre_indicador).execute()
                            print(f"    ↻ {nombre_indicador} (actualizado)")
                        else:
                            raise insert_error
                except Exception as e:
                    print(f"    ⚠️  Error con {nombre_indicador}: {e}")
                
                # Insertar resultados
                resultados_batch = []
                for _, row in df.iterrows():
                    try:
                        # Determinar valor
                        valor = 0
                        for col in ['valor', 'Valor', 'value', 'Value']:
                            if col in row:
                                try:
                                    valor = float(row[col])
                                    break
                                except:
                                    pass
                        
                        # Determinar país
                        pais = 'España'
                        for col in ['pais', 'Pais', 'geo', 'país', 'País', 'country', 'Country']:
                            if col in row and pd.notna(row[col]):
                                pais = str(row[col])
                                break
                        
                        # Determinar periodo
                        periodo = 2024
                        for col in ['periodo', 'año', 'anio', 'time', 'year', 'Year']:
                            if col in row and pd.notna(row[col]):
                                try:
                                    periodo = int(row[col])
                                    break
                                except:
                                    pass
                        
                        # Determinar provincia (opcional)
                        provincia = None
                        for col in ['provincia', 'Provincia', 'province', 'Province']:
                            if col in row and pd.notna(row[col]):
                                provincia = str(row[col])
                                break
                        
                        resultado = {
                            'nombre_indicador': nombre_indicador,
                            'valor_calculado': float(valor),
                            'pais': pais,
                            'periodo': periodo
                        }
                        
                        if provincia:
                            resultado['provincia'] = provincia
                        
                        resultados_batch.append(resultado)
                        
                        # Insertar en lotes de 50
                        if len(resultados_batch) >= 50:
                            try:
                                supabase.table('resultado_indicadores').insert(resultados_batch).execute()
                                total_resultados += len(resultados_batch)
                                resultados_batch = []
                            except Exception as e:
                                print(f"    ⚠️  Error batch: {e}")
                                resultados_batch = []
                    
                    except Exception as e:
                        pass
                
                # Insertar batch final
                if resultados_batch:
                    try:
                        supabase.table('resultado_indicadores').insert(resultados_batch).execute()
                        total_resultados += len(resultados_batch)
                    except Exception as e:
                        print(f"    ⚠️  Error batch final: {e}")
                
                indicadores_procesados.add(nombre_indicador)
                
            except Exception as e:
                print(f"    ❌ Error procesando {csv_file.name}: {e}")
    
    print(f"\n✅ Total indicadores procesados: {total_indicadores}")
    print(f"✅ Total resultados cargados: {total_resultados}")
    return len(indicadores_procesados)

def load_indicadores_from_catalog():
    """Carga indicadores desde el catálogo de indicadores del backend"""
    print("\n📚 Cargando indicadores desde catálogo...")
    
    try:
        # Importar el catálogo de indicadores
        import sys
        sys.path.insert(0, str(BACKEND_DIR))
        
        from data.processed.indicadores.indicators import CATALOGO_COMPLETO
        
        total_catalog = 0
        for nombre, indicador in CATALOGO_COMPLETO.items():
            try:
                # Obtener información del indicador
                dimension = indicador.dimension.value if hasattr(indicador.dimension, 'value') else str(indicador.dimension)
                subdimension = indicador.subdimension.value if hasattr(indicador.subdimension, 'value') else str(indicador.subdimension)
                origen = indicador.origen if hasattr(indicador, 'origen') else 'Otro'
                importancia = indicador.importancia if hasattr(indicador, 'importancia') else 'Media'
                formula = indicador.formula_calculo if hasattr(indicador, 'formula_calculo') else 'Dato crudo'
                
                indicador_data = {
                    'nombre': nombre,
                    'formula': formula,
                    'origen_indicador': origen,
                    'nombre_subdimension': subdimension,
                    'importancia': importancia
                }
                
                supabase.table('definicion_indicadores').insert(indicador_data).execute()
                total_catalog += 1
                print(f"  ✓ {nombre}")
            except Exception as e:
                if 'duplicate key' not in str(e).lower() and 'unique constraint' not in str(e).lower():
                    print(f"  ⚠️  {nombre}: {e}")
        
        print(f"\n✅ Total indicadores del catálogo: {total_catalog}")
        return total_catalog
    except Exception as e:
        print(f"⚠️  No se pudo cargar el catálogo: {e}")
        return 0

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 CARGA COMPLETA DE TODOS LOS INDICADORES")
    print("=" * 60)
    
    try:
        # 1. Cargar desde CSVs
        csv_count = load_indicadores_from_csv()
        
        # 2. Cargar desde catálogo
        catalog_count = load_indicadores_from_catalog()
        
        print("\n" + "=" * 60)
        print("✅ CARGA COMPLETADA")
        print("=" * 60)
        print(f"📊 Indicadores desde CSVs: {csv_count}")
        print(f"📚 Indicadores desde catálogo: {catalog_count}")
        
        # Mostrar resumen
        print("\n📊 RESUMEN FINAL:")
        for table in ['definicion_indicadores', 'resultado_indicadores']:
            try:
                count_result = supabase.table(table).select('nombre', count='exact').limit(1).execute()
                count = count_result.count if hasattr(count_result, 'count') else len(count_result.data) if count_result.data else 0
                print(f"  • {table}: ~{count}+ registros")
            except Exception as e:
                print(f"  • {table}: Error contando")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

