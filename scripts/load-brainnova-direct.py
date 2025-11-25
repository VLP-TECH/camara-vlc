#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para cargar datos de Brainnova en Supabase
Usa requests para ejecutar SQL directamente
"""

import os
import sys
import requests
from supabase import create_client, Client

# Configuración de Supabase
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "https://aoykpiievtadhwssugvs.supabase.co")
SUPABASE_ANON_KEY = os.getenv("VITE_SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

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
    """Habilita las políticas de inserción usando la API REST de Supabase"""
    print("🔓 Habilitando políticas de inserción...")
    
    policies = [
        ("dimensiones", "Dimensiones"),
        ("subdimensiones", "Subdimensiones"),
        ("definicion_indicadores", "Definición de indicadores"),
        ("componentes_indicador", "Componentes de indicador"),
        ("resultado_indicadores", "Resultado de indicadores"),
        ("datos_crudos", "Datos crudos"),
        ("datos_macro", "Datos macro"),
    ]
    
    for table, name in policies:
        sql = f'''
        DROP POLICY IF EXISTS "Allow insert for data loading" ON public.{table};
        CREATE POLICY "Allow insert for data loading"
        ON public.{table} FOR INSERT
        WITH CHECK (true);
        '''
        
        # Intentar ejecutar usando la API REST de Supabase
        # Nota: Esto requiere permisos especiales, puede que no funcione con anon key
        try:
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
                headers={
                    "apikey": SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    "Content-Type": "application/json"
                },
                json={"sql": sql}
            )
            if response.status_code == 200:
                print(f"   ✅ {name}")
            else:
                print(f"   ⚠️  {name}: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  {name}: No se pudo ejecutar automáticamente")
    
    print("   💡 Si las políticas no se habilitaron, ejecuta manualmente:")
    print("      scripts/enable-data-insertion.sql en Supabase SQL Editor")


def load_dimensiones():
    """Carga las dimensiones en Supabase"""
    print("📊 Cargando dimensiones...")
    
    try:
        result = supabase.table("dimensiones").upsert(DIMENSIONES, on_conflict="nombre").execute()
        print(f"✅ {len(DIMENSIONES)} dimensiones cargadas")
        return result
    except Exception as e:
        error_msg = str(e)
        if "row-level security" in error_msg.lower():
            print("   ⚠️  Error de RLS. Las políticas deben habilitarse primero.")
            print("   📋 Ejecuta este SQL en Supabase:")
            print("      https://supabase.com/dashboard/project/aoykpiievtadhwssugvs/sql/new")
            print()
            print("   O copia y pega el contenido de: scripts/enable-data-insertion.sql")
            raise Exception("RLS bloquea la inserción. Ejecuta el SQL de habilitación primero.")
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
    print("🚀 Iniciando carga de datos en Supabase...\n")
    
    # Intentar habilitar políticas primero
    enable_insert_policies()
    print()
    
    try:
        # 1. Cargar dimensiones
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
        print("   2. Copia y pega el contenido de: scripts/enable-data-insertion.sql")
        print("   3. Ejecuta el SQL (botón 'Run')")
        print("   4. Vuelve a ejecutar este script")
        sys.exit(1)


if __name__ == "__main__":
    main()

