#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar qué indicadores hay en Supabase"""

from supabase import create_client

supabase = create_client(
    'https://aoykpiievtadhwssugvs.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY'
)

# Obtener todos los indicadores desde definicion_indicadores
result = supabase.table('definicion_indicadores').select('nombre').execute()

if result.data:
    indicadores = sorted([i['nombre'] for i in result.data])
    print(f"\n📊 Total indicadores en Supabase: {len(indicadores)}\n")
    print("Lista completa:")
    for i, ind in enumerate(indicadores, 1):
        print(f"  {i}. {ind}")
else:
    print("❌ No hay indicadores en definicion_indicadores")

