#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script completo para cargar todos los datos de Brainnova en Supabase:
- Componentes de indicadores
- Datos crudos
- Datos macro
- Resultados de indicadores
"""

import os
import sys
import csv
from pathlib import Path
from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "https://aoykpiievtadhwssugvs.supabase.co")
SUPABASE_ANON_KEY = os.getenv("VITE_SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

BACKEND_DIR = Path("/Users/chaumesanchez/Downloads/Camara_de_comercio")

# Mapeo de archivos unfiltered a indicadores/nombres
UNFILTERED_MAPPING = {
    'suscripciones_banda_ancha_fija': {
        'nombre_indicador': 'Adopción de banda ancha fija (suscripciones/100 personas)',
        'descripcion_dato': 'Nº total de suscripciones de banda ancha fija',
        'campo_valor': 'lineas_o_accesos'
    },
    'suscripciones_datos_moviles': {
        'nombre_indicador': 'Adopción de banda ancha móvil (suscripciones/100 personas)',
        'descripcion_dato': 'Nº total de suscripciones activas de datos móviles',
        'campo_valor': 'lineas_o_accesos'
    },
    'precio_banda_ancha': {
        'nombre_indicador': 'Precio relativo de banda ancha',
        'descripcion_dato': 'Precio mensual del servicio de banda ancha en euros',
        'campo_valor': 'ingresos'
    }
}


def parse_roles_file():
    """Parsea el archivo roles.py para extraer componentes"""
    componentes = []
    roles_file = BACKEND_DIR / "data/processed/indicadores/roles.py"
    
    if not roles_file.exists():
        print(f"⚠️  Archivo no encontrado: {roles_file}")
        return componentes
    
    try:
        with open(roles_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        
        # Buscar cada entrada del catálogo - patrón más flexible
        pattern = r"\{'nombre_indicador':\s*'([^']+)',\s*'componentes':\s*\[(.*?)\]\}"
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            nombre_indicador = match.group(1)
            componentes_str = match.group(2)
            
            # Buscar componentes individuales - patrón más flexible
            comp_pattern = r"\{'descripcion_dato':\s*'([^']*)'[^}]*'rol':\s*'([^']*)'"
            comp_matches = re.finditer(comp_pattern, componentes_str)
            
            for comp_match in comp_matches:
                descripcion_dato = comp_match.group(1)
                rol = comp_match.group(2)
                
                if descripcion_dato and descripcion_dato != 'nan':
                    # Determinar fuente_tabla basado en el rol y descripción
                    fuente_tabla = "DATOS_CRUDOS"  # Por defecto
                    if "Población" in descripcion_dato or "poblacion" in descripcion_dato.lower():
                        fuente_tabla = "DATOS_MACRO"
                    
                    componentes.append({
                        "nombre_indicador": nombre_indicador,
                        "descripcion_dato": descripcion_dato[:100] if len(descripcion_dato) > 100 else descripcion_dato,
                        "fuente_tabla": fuente_tabla[:100] if len(fuente_tabla) > 100 else fuente_tabla
                    })
        
        return componentes
    
    except Exception as e:
        print(f"❌ Error parseando roles.py: {e}")
        import traceback
        traceback.print_exc()
        return []


def load_componentes():
    """Carga los componentes de indicadores"""
    print("📊 Cargando componentes de indicadores...")
    
    componentes = parse_roles_file()
    
    if not componentes:
        print("⚠️  No se encontraron componentes")
        return []
    
    print(f"   📋 Encontrados {len(componentes)} componentes")
    
    # Obtener lista de indicadores existentes en la BD
    try:
        indicadores_response = supabase.table("definicion_indicadores").select("nombre").execute()
        indicadores_existentes = {ind["nombre"] for ind in indicadores_response.data}
        print(f"   📋 {len(indicadores_existentes)} indicadores existentes en la BD")
    except Exception as e:
        print(f"   ⚠️  No se pudieron obtener indicadores existentes: {e}")
        indicadores_existentes = set()
    
    # Filtrar componentes que tienen indicadores existentes
    componentes_validos = [
        comp for comp in componentes 
        if comp["nombre_indicador"] in indicadores_existentes
    ]
    
    print(f"   📋 {len(componentes_validos)} componentes válidos (con indicador existente)")
    
    if not componentes_validos:
        print("⚠️  No hay componentes válidos para cargar")
        return []
    
    try:
        # Insertar en lotes de 500
        batch_size = 500
        total_inserted = 0
        
        for i in range(0, len(componentes_validos), batch_size):
            batch = componentes_validos[i:i + batch_size]
            result = supabase.table("componentes_indicador").insert(batch).execute()
            total_inserted += len(batch)
            print(f"   ✅ Lote {i//batch_size + 1}: {len(batch)} componentes")
        
        print(f"✅ {total_inserted} componentes cargados")
        return componentes_validos
    
    except Exception as e:
        print(f"❌ Error cargando componentes: {e}")
        raise


def get_indicador_name_from_filename(filename):
    """Extrae el nombre del indicador del nombre del archivo"""
    # Mapeo directo de nombres de archivo a indicadores
    mapeo = {
        'empresas_uso_ia': 'Empresas que usan inteligencia artificial',
        'empresas_big_data': 'Empresas que analizan big data de cualquier fuente de datos',
        'empresas_erp_procesos_internos': 'Empresas que comparten información electrónica internamente con un ERP',
        'empresas_presencia_web_propia': 'Empresas que tienen un sitio web o página de inicio',
        'empresas_venta_online': 'Empresas que utilizan el mercado de comercio electrónico para ventas',
        'empresas_uso_redes_sociales': 'Empresas que utilizan las redes sociales',
        'empresas_formacion_empleados_tic': 'Formación en TIC en empresas',
        'empresas_permiten_teletrabajo': 'Teletrabajo',
        'empresas_servicios_cloud_computing': 'Empresas con infraestructura en la nube',
        'empresas_tic_actividades_i+d': 'Número de empresas que realizan I+D en el sector TIC',
        'empresas_usan_crm': 'Empresas que utilizan software de gestión de relaciones con los clientes (CRM)',
        'habilidades_digitales_basicas': 'Personas con habilidades digitales básicas',
        'habilidades_digitales_superior_a_basica': 'Personas con habilidades digitales generales superiores a las básicas',
        'interaccion_autoridades_publicas': 'Personas que interactúan en línea con las autoridades públicas',
        'personas_servicio_banca_electronica': 'Usuarios que usan banca online',
        'personas_uso_internet_una_vez_semana': 'Uso regular de Internet',
        'cobertura_de_redes_vhcn': 'Cobertura de redes de muy alta capacidad (VHCN)',
    }
    
    filename_base = filename.lower().replace('.csv', '').replace('filtered/', '').replace('resultado/', '')
    
    # Buscar coincidencia exacta primero
    for key, indicador in mapeo.items():
        if key in filename_base:
            return indicador
    
    # Si no hay coincidencia, buscar en la BD
    try:
        indicadores_response = supabase.table("definicion_indicadores").select("nombre").execute()
        indicadores = [ind["nombre"] for ind in indicadores_response.data]
        
        # Buscar coincidencias parciales
        palabras_clave = filename_base.replace('_', ' ').split()
        for indicador in indicadores:
            indicador_lower = indicador.lower()
            if any(palabra in indicador_lower for palabra in palabras_clave if len(palabra) > 4):
                return indicador
    except:
        pass
    
    return None


def load_csv_data(table_name, csv_path, mapping_func, metadata=None):
    """Carga datos desde un CSV a una tabla"""
    if not csv_path.exists():
        print(f"⚠️  Archivo no encontrado: {csv_path}")
        return []
    
    print(f"📊 Cargando {table_name} desde {csv_path.name}...")
    
    datos = []
    
    # Para resultados, intentar obtener nombre_indicador del archivo
    nombre_indicador_archivo = None
    if table_name == "resultado_indicadores":
        nombre_indicador_archivo = get_indicador_name_from_filename(csv_path.name)
        if nombre_indicador_archivo:
            print(f"   📋 Indicador detectado: {nombre_indicador_archivo}")
    
    # Para datos crudos unfiltered, obtener metadata
    file_metadata = metadata
    if not file_metadata and table_name == "datos_crudos":
        filename_lower = csv_path.name.lower().replace('.csv', '')
        for key, meta in UNFILTERED_MAPPING.items():
            if key in filename_lower:
                file_metadata = meta
                print(f"   📋 Metadata detectada: {meta['nombre_indicador']}")
                break
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Detectar delimitador
            first_line = f.readline()
            f.seek(0)
            
            delimiter = ';' if ';' in first_line else ','
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for row in reader:
                if table_name == "resultado_indicadores":
                    mapped_data = mapping_func(row, nombre_indicador_archivo)
                elif table_name == "datos_crudos" and file_metadata:
                    mapped_data = mapping_func(row, file_metadata)
                else:
                    mapped_data = mapping_func(row)
                if mapped_data:
                    datos.append(mapped_data)
        
        if not datos:
            print(f"   ⚠️  No se encontraron datos válidos")
            return []
        
        print(f"   📋 Encontrados {len(datos)} registros")
        
        # Insertar en lotes de 1000
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(datos), batch_size):
            batch = datos[i:i + batch_size]
            try:
                result = supabase.table(table_name).insert(batch).execute()
                total_inserted += len(batch)
                print(f"   ✅ Lote {i//batch_size + 1}: {len(batch)} registros")
            except Exception as e:
                print(f"   ⚠️  Error en lote {i//batch_size + 1}: {e}")
                # Continuar con el siguiente lote
        
        print(f"✅ {total_inserted} registros cargados en {table_name}")
        return datos
    
    except Exception as e:
        print(f"❌ Error cargando {table_name}: {e}")
        import traceback
        traceback.print_exc()
        return []


def map_datos_crudos(row, metadata=None):
    """Mapea una fila de CSV a datos_crudos"""
    try:
        # Si hay metadata (para archivos unfiltered), usarla
        nombre_indicador = None
        descripcion_dato = None
        campo_valor = 'valor'
        
        if metadata:
            nombre_indicador = metadata.get('nombre_indicador')
            descripcion_dato = metadata.get('descripcion_dato')
            campo_valor = metadata.get('campo_valor', 'valor')
        
        # Buscar valor en diferentes campos
        valor = None
        if campo_valor in row:
            try:
                valor = float(row[campo_valor]) if row[campo_valor] and str(row[campo_valor]).strip() else None
            except:
                pass
        
        if valor is None:
            # Intentar campos comunes
            for key in ['valor', 'unidades', 'lineas_o_accesos', 'ingresos', 'value']:
                if key in row:
                    try:
                        valor = float(row[key]) if row[key] and str(row[key]).strip() else None
                        if valor is not None:
                            break
                    except:
                        continue
        
        if valor is None:
            return None
        
        # Buscar periodo/año
        periodo = None
        for key in ['periodo', 'anno', 'año', 'year', 'period']:
            if key in row:
                try:
                    periodo = int(row[key]) if row[key] else None
                    if periodo:
                        break
                except:
                    continue
        
        if not periodo:
            return None
        
        return {
            "nombre_indicador": nombre_indicador or row.get('nombre_indicador', '').strip() or None,
            "valor": valor,
            "unidad": row.get('unidad', '').strip()[:30] if row.get('unidad') else None,
            "pais": row.get('pais', 'España').strip()[:30] if row.get('pais') else 'España',
            "provincia": row.get('provincia', '').strip()[:30] if row.get('provincia') else None,
            "periodo": periodo,
            "descripcion_dato": descripcion_dato or row.get('descripcion_dato', '').strip()[:50] if row.get('descripcion_dato') else None
        }
    except (ValueError, KeyError, AttributeError) as e:
        return None


def map_datos_macro(row):
    """Mapea una fila de CSV a datos_macro"""
    try:
        return {
            "valor": float(row.get('valor', 0)) if row.get('valor') else None,
            "unidad": row.get('unidad', '').strip()[:30] if row.get('unidad') else None,
            "pais": row.get('pais', '').strip()[:30] if row.get('pais') else None,
            "provincia": row.get('provincia', '').strip()[:30] if row.get('provincia') else None,
            "periodo": int(row.get('periodo', 0)) if row.get('periodo') else None,
            "descripcion_dato": row.get('descripcion_dato', '').strip()[:50] if row.get('descripcion_dato') else None
        }
    except (ValueError, KeyError) as e:
        return None


def map_resultados(row, nombre_indicador=None):
    """Mapea una fila de CSV a resultado_indicadores"""
    try:
        if not nombre_indicador:
            return None
        
        # Buscar valor en diferentes campos posibles (columnas con % o value)
        valor = None
        for key in row.keys():
            if '%' in key or 'value' in key.lower() or key.startswith('%'):
                try:
                    valor = float(row[key]) if row[key] and str(row[key]).strip() else None
                    break
                except:
                    continue
        
        if valor is None:
            # Intentar con campos comunes
            valor = (row.get('valor') or 
                    row.get('valor_calculado') or 
                    row.get('resultado') or
                    row.get('percentage'))
            try:
                valor = float(valor) if valor and str(valor).strip() else None
            except:
                valor = None
        
        if valor is None:
            return None
        
        return {
            "nombre_indicador": nombre_indicador,
            "valor_calculado": valor,
            "pais": row.get('pais', '').strip()[:30] if row.get('pais') else None,
            "provincia": row.get('provincia', '').strip()[:30] if row.get('provincia') else None,
            "periodo": int(row.get('periodo', 0)) if row.get('periodo') else None
        }
    except (ValueError, KeyError, AttributeError, TypeError) as e:
        return None


def load_all_csv_data():
    """Carga todos los datos desde los CSV procesados"""
    print("\n📁 Buscando archivos CSV procesados...\n")
    
    processed_dir = BACKEND_DIR / "data/processed"
    
    # Buscar datos crudos usando glob recursivo (también en unfiltered y raw)
    crudos_files = (list(processed_dir.rglob("**/filtered/crudo/*.csv")) + 
                   list(processed_dir.rglob("**/unfiltered/crudo/*.csv")) +
                   list(processed_dir.rglob("**/unfiltered/*.csv")))
    
    # Eliminar duplicados
    crudos_files = list(set(crudos_files))
    
    # Buscar datos macro (pueden estar en diferentes ubicaciones)
    macro_files = (list(processed_dir.rglob("**/macro/*.csv")) +
                  list(processed_dir.rglob("**/filtered/macro/*.csv")))
    macro_files = list(set(macro_files))
    
    # Buscar resultados (también en unfiltered)
    resultados_files = (list(processed_dir.rglob("**/filtered/resultado/*.csv")) +
                       list(processed_dir.rglob("**/unfiltered/resultado/*.csv")))
    resultados_files = list(set(resultados_files))
    
    print(f"   📋 Encontrados:")
    print(f"      - {len(crudos_files)} archivos de datos crudos")
    print(f"      - {len(macro_files)} archivos de datos macro")
    print(f"      - {len(resultados_files)} archivos de resultados\n")
    
    # Cargar datos crudos (todos los archivos)
    total_crudos = 0
    for csv_file in crudos_files:
        datos = load_csv_data("datos_crudos", csv_file, map_datos_crudos)
        total_crudos += len(datos) if datos else 0
    
    # Cargar datos macro (todos los archivos)
    total_macro = 0
    for csv_file in macro_files:
        datos = load_csv_data("datos_macro", csv_file, map_datos_macro)
        total_macro += len(datos) if datos else 0
    
    # Cargar resultados (todos los archivos)
    total_resultados = 0
    for csv_file in resultados_files:
        datos = load_csv_data("resultado_indicadores", csv_file, map_resultados)
        total_resultados += len(datos) if datos else 0
    
    print(f"\n📊 Resumen:")
    print(f"   - Datos crudos: {total_crudos} registros")
    print(f"   - Datos macro: {total_macro} registros")
    print(f"   - Resultados: {total_resultados} registros")


def main():
    """Función principal"""
    print("🚀 Iniciando carga completa de datos en Supabase...\n")
    
    try:
        # 1. Cargar componentes
        load_componentes()
        print()
        
        # 2. Cargar datos desde CSV
        load_all_csv_data()
        
        print("\n✅ Carga completa finalizada")
        
    except Exception as e:
        print(f"\n❌ Error durante la carga: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

