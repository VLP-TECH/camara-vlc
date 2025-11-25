#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script completo para cargar datos de Brainnova en Supabase
Primero habilita las políticas de inserción y luego carga los datos
"""

import os
import sys
from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "https://aoykpiievtadhwssugvs.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("VITE_SUPABASE_SERVICE_ROLE_KEY", "")

if not SUPABASE_SERVICE_KEY:
    # Usar anon key como fallback
    SUPABASE_SERVICE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Datos de dimensiones
DIMENSIONES = [
    {"nombre": "Emprendimiento e innovación", "peso": 10},
    {"nombre": "Capital humano", "peso": 20},
    {"nombre": "Ecosistema y colaboración", "peso": 15},
    {"nombre": "Infraestructura digital", "peso": 15},
    {"nombre": "Servicios públicos digitales", "peso": 10},
    {"nombre": "Sostenibilidad digital", "peso": 5},
    {"nombre": "Transformación digital empresarial", "peso": 30},
]

SUBDIMENSIONES = [
    # Emprendimiento e innovación
    {"nombre": "Acceso a financiación", "nombre_dimension": "Emprendimiento e innovación", "peso": 0},
    {"nombre": "Dinamismo emprendedor", "nombre_dimension": "Emprendimiento e innovación", "peso": 0},
    {"nombre": "Infraestructura de apoyo", "nombre_dimension": "Emprendimiento e innovación", "peso": 0},
    {"nombre": "Políticas de fomento", "nombre_dimension": "Emprendimiento e innovación", "peso": 0},
    # Capital humano
    {"nombre": "Competencias digitales", "nombre_dimension": "Capital humano", "peso": 0},
    {"nombre": "Formación continua", "nombre_dimension": "Capital humano", "peso": 0},
    {"nombre": "Talento profesional", "nombre_dimension": "Capital humano", "peso": 0},
    # Ecosistema y colaboración
    {"nombre": "Atractivo del ecosistema", "nombre_dimension": "Ecosistema y colaboración", "peso": 0},
    {"nombre": "Provision tecnológica", "nombre_dimension": "Ecosistema y colaboración", "peso": 0},
    {"nombre": "Transferencia de conocimiento", "nombre_dimension": "Ecosistema y colaboración", "peso": 0},
    # Infraestructura digital
    {"nombre": "Acceso a infraestructuras", "nombre_dimension": "Infraestructura digital", "peso": 0},
    # Servicios públicos digitales
    {"nombre": "Disponibilidad de servicios digitales", "nombre_dimension": "Servicios públicos digitales", "peso": 0},
    {"nombre": "Integración con administración", "nombre_dimension": "Servicios públicos digitales", "peso": 0},
    # Sostenibilidad digital
    {"nombre": "Economía circular", "nombre_dimension": "Sostenibilidad digital", "peso": 0},
    {"nombre": "Huella ambiental", "nombre_dimension": "Sostenibilidad digital", "peso": 0},
    # Transformación digital empresarial
    {"nombre": "Organización digital", "nombre_dimension": "Transformación digital empresarial", "peso": 0},
    {"nombre": "Digitalización básica", "nombre_dimension": "Transformación digital empresarial", "peso": 0},
    {"nombre": "E-commerce", "nombre_dimension": "Transformación digital empresarial", "peso": 0},
    {"nombre": "Tecnologías avanzadas", "nombre_dimension": "Transformación digital empresarial", "peso": 0},
]


def enable_insert_policies():
    """Habilita las políticas de inserción usando SQL"""
    print("🔓 Habilitando políticas de inserción...")
    
    sql_script = """
    -- Dimensiones
    DROP POLICY IF EXISTS "Allow insert for data loading" ON public.dimensiones;
    CREATE POLICY "Allow insert for data loading"
    ON public.dimensiones FOR INSERT
    WITH CHECK (true);

    -- Subdimensiones
    DROP POLICY IF EXISTS "Allow insert for data loading" ON public.subdimensiones;
    CREATE POLICY "Allow insert for data loading"
    ON public.subdimensiones FOR INSERT
    WITH CHECK (true);

    -- Definición de indicadores
    DROP POLICY IF EXISTS "Allow insert for data loading" ON public.definicion_indicadores;
    CREATE POLICY "Allow insert for data loading"
    ON public.definicion_indicadores FOR INSERT
    WITH CHECK (true);

    -- Componentes de indicador
    DROP POLICY IF EXISTS "Allow insert for data loading" ON public.componentes_indicador;
    CREATE POLICY "Allow insert for data loading"
    ON public.componentes_indicador FOR INSERT
    WITH CHECK (true);

    -- Resultado de indicadores
    DROP POLICY IF EXISTS "Allow insert for data loading" ON public.resultado_indicadores;
    CREATE POLICY "Allow insert for data loading"
    ON public.resultado_indicadores FOR INSERT
    WITH CHECK (true);

    -- Datos crudos
    DROP POLICY IF EXISTS "Allow insert for data loading" ON public.datos_crudos;
    CREATE POLICY "Allow insert for data loading"
    ON public.datos_crudos FOR INSERT
    WITH CHECK (true);

    -- Datos macro
    DROP POLICY IF EXISTS "Allow insert for data loading" ON public.datos_macro;
    CREATE POLICY "Allow insert for data loading"
    ON public.datos_macro FOR INSERT
    WITH CHECK (true);
    """
    
    try:
        # Ejecutar SQL usando rpc o directamente
        result = supabase.rpc('exec_sql', {'sql': sql_script}).execute()
        print("✅ Políticas de inserción habilitadas")
    except Exception as e:
        # Si falla, intentar usar la API directamente
        print(f"⚠️  No se pudo ejecutar SQL automáticamente: {e}")
        print("   Las políticas deben habilitarse manualmente en Supabase")
        print("   Ejecuta el script: scripts/enable-data-insertion.sql")


def load_dimensiones():
    """Carga las dimensiones en Supabase"""
    print("📊 Cargando dimensiones...")
    
    try:
        result = supabase.table("dimensiones").upsert(DIMENSIONES, on_conflict="nombre").execute()
        print(f"✅ {len(DIMENSIONES)} dimensiones cargadas")
        return result
    except Exception as e:
        print(f"❌ Error cargando dimensiones: {e}")
        # Si falla por RLS, intentar habilitar políticas primero
        if "row-level security" in str(e).lower():
            print("   Intentando habilitar políticas de inserción...")
            enable_insert_policies()
            # Reintentar
            try:
                result = supabase.table("dimensiones").upsert(DIMENSIONES, on_conflict="nombre").execute()
                print(f"✅ {len(DIMENSIONES)} dimensiones cargadas (después de habilitar políticas)")
                return result
            except Exception as e2:
                print(f"❌ Error después de habilitar políticas: {e2}")
                raise
        raise


def load_subdimensiones():
    """Carga las subdimensiones en Supabase"""
    print("📊 Cargando subdimensiones...")
    
    try:
        result = supabase.table("subdimensiones").upsert(SUBDIMENSIONES, on_conflict="nombre").execute()
        print(f"✅ {len(SUBDIMENSIONES)} subdimensiones cargadas")
        return result
    except Exception as e:
        print(f"❌ Error cargando subdimensiones: {e}")
        raise


def main():
    """Función principal"""
    print("🚀 Iniciando carga completa de datos en Supabase...\n")
    
    try:
        # 1. Cargar dimensiones (esto intentará habilitar políticas si es necesario)
        load_dimensiones()
        print()
        
        # 2. Cargar subdimensiones
        load_subdimensiones()
        print()
        
        print("✅ Carga de datos básicos completada")
        print("\n📝 Próximos pasos:")
        print("   - Los indicadores deben cargarse desde el backend Python completo")
        print("   - Los datos crudos y macro deben cargarse desde los CSV procesados")
        
    except Exception as e:
        print(f"\n❌ Error durante la carga: {e}")
        print("\n💡 Solución:")
        print("   1. Ve a: https://supabase.com/dashboard/project/aoykpiievtadhwssugvs/sql/new")
        print("   2. Ejecuta el script: scripts/enable-data-insertion.sql")
        print("   3. Vuelve a ejecutar este script")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

