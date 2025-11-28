#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para cargar datos básicos a Supabase
Solo carga campos que existen en las tablas actuales
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

def load_indicadores_simple():
    """Carga indicadores usando solo campos básicos"""
    print("\n📈 Cargando indicadores básicos...")
    
    result_dirs = [
        DATA_DIR / "eurostat" / "filtered" / "resultado",
        DATA_DIR / "ine" / "filtered" / "resultado",
        DATA_DIR / "digital_decade" / "filtered" / "resultado",
    ]
    
    total_indicadores = 0
    total_resultados = 0
    indicadores_procesados = set()
    
    for result_dir in result_dirs:
        if not result_dir.exists():
            continue
            
        for csv_file in result_dir.glob("*.csv"):
            try:
                nombre_indicador = csv_file.stem.replace('_', ' ').title()
                
                if nombre_indicador in indicadores_procesados:
                    continue
                
                # Leer CSV
                df = pd.read_csv(csv_file)
                
                if len(df) == 0:
                    continue
                
                # Insertar definición (solo campos básicos)
                try:
                    indicador_data = {
                        'nombre': nombre_indicador,
                        'formula': 'Dato crudo',
                        'origen_indicador': determinar_origen(csv_file.parent.parent.parent.name),
                        'nombre_subdimension': determinar_subdimension(nombre_indicador),
                        'importancia': 'Media'
                    }
                    supabase.table('definicion_indicadores').insert(indicador_data).execute()
                    total_indicadores += 1
                    print(f"  ✓ {nombre_indicador}")
                except Exception as e:
                    if 'duplicate key' not in str(e).lower():
                        print(f"  ⚠️  Definición {nombre_indicador}: {e}")
                
                # Insertar resultados (solo campos básicos)
                resultados_batch = []
                for _, row in df.iterrows():
                    try:
                        # Determinar valor
                        valor = 0
                        for col in ['valor', 'Valor', 'value', 'Value']:
                            if col in row:
                                valor = float(row[col])
                                break
                        
                        # Determinar país
                        pais = 'España'
                        for col in ['pais', 'Pais', 'geo', 'país', 'País']:
                            if col in row and pd.notna(row[col]):
                                pais = str(row[col])
                                break
                        
                        # Determinar periodo
                        periodo = 2024
                        for col in ['periodo', 'año', 'anio', 'time', 'year']:
                            if col in row and pd.notna(row[col]):
                                try:
                                    periodo = int(row[col])
                                    break
                                except:
                                    pass
                        
                        # Determinar provincia (opcional)
                        provincia = None
                        for col in ['provincia', 'Provincia', 'province']:
                            if col in row and pd.notna(row[col]):
                                provincia = str(row[col])
                                break
                        
                        resultado = {
                            'nombre_indicador': nombre_indicador,
                            'valor_calculado': float(valor),
                            'pais': pais,
                            'periodo': periodo
                        }
                        
                        # Añadir provincia solo si existe
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
                                print(f"  ⚠️  Error batch: {e}")
                                resultados_batch = []
                    
                    except Exception as e:
                        pass  # Ignorar filas con errores
                
                # Insertar batch final
                if resultados_batch:
                    try:
                        supabase.table('resultado_indicadores').insert(resultados_batch).execute()
                        total_resultados += len(resultados_batch)
                    except Exception as e:
                        print(f"  ⚠️  Error batch final: {e}")
                
                indicadores_procesados.add(nombre_indicador)
                
            except Exception as e:
                print(f"  ❌ Error procesando {csv_file.name}: {e}")
    
    print(f"\n✅ Total indicadores: {total_indicadores}")
    print(f"✅ Total resultados: {total_resultados}")

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
        return 'Digitalización Básica'

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

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 CARGA SIMPLIFICADA DE DATOS BRAINNOVA")
    print("=" * 60)
    
    try:
        load_indicadores_simple()
        
        print("\n" + "=" * 60)
        print("✅ CARGA COMPLETADA")
        print("=" * 60)
        
        # Mostrar resumen
        print("\n📊 RESUMEN:")
        for table in ['dimensiones', 'subdimensiones', 'definicion_indicadores', 'resultado_indicadores']:
            try:
                count_result = supabase.table(table).select('nombre', count='exact').limit(1).execute()
                count = count_result.count if hasattr(count_result, 'count') else len(count_result.data)
                print(f"  • {table}: ~{count}+ registros")
            except Exception as e:
                print(f"  • {table}: Error contando")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

