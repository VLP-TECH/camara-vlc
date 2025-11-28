#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para listar indicadores que tienen datos asociados a países
"""

from supabase import create_client
from collections import defaultdict

supabase = create_client(
    'https://aoykpiievtadhwssugvs.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY'
)

def main():
    print("=" * 80)
    print("📊 LISTADO DE INDICADORES CON DATOS POR PAÍS")
    print("=" * 80)
    
    # Obtener todos los resultados con indicador y país
    print("\n🔍 Consultando resultado_indicadores...")
    result = supabase.table('resultado_indicadores').select('nombre_indicador, pais, periodo').execute()
    
    if not result.data:
        print("❌ No hay datos en resultado_indicadores")
        return
    
    # Agrupar por indicador y país
    indicadores_paises = defaultdict(lambda: defaultdict(set))
    total_registros = len(result.data)
    
    for registro in result.data:
        indicador = registro.get('nombre_indicador', '').strip()
        pais = registro.get('pais', '').strip()
        periodo = registro.get('periodo')
        
        if indicador and pais:
            indicadores_paises[indicador][pais].add(periodo)
    
    # Ordenar indicadores alfabéticamente
    indicadores_ordenados = sorted(indicadores_paises.keys())
    
    print(f"\n✅ Total de registros procesados: {total_registros}")
    print(f"✅ Total de indicadores únicos con datos: {len(indicadores_ordenados)}\n")
    
    # Mostrar listado detallado
    print("=" * 80)
    print("📋 DETALLE POR INDICADOR:")
    print("=" * 80)
    
    for i, indicador in enumerate(indicadores_ordenados, 1):
        paises = indicadores_paises[indicador]
        total_paises = len(paises)
        total_periodos = sum(len(periodos) for periodos in paises.values())
        
        print(f"\n{i}. {indicador}")
        print(f"   📍 Países: {total_paises} | 📅 Períodos únicos: {total_periodos}")
        print(f"   Países disponibles:")
        
        for pais in sorted(paises.keys()):
            periodos = sorted(paises[pais])
            periodos_str = ', '.join(map(str, periodos[:5]))
            if len(periodos) > 5:
                periodos_str += f", ... (+{len(periodos) - 5} más)"
            print(f"      • {pais}: {len(periodos)} períodos ({periodos_str})")
    
    # Resumen por país
    print("\n" + "=" * 80)
    print("🌍 RESUMEN POR PAÍS:")
    print("=" * 80)
    
    paises_indicadores = defaultdict(set)
    for indicador, paises in indicadores_paises.items():
        for pais in paises.keys():
            paises_indicadores[pais].add(indicador)
    
    for pais in sorted(paises_indicadores.keys()):
        indicadores = paises_indicadores[pais]
        print(f"\n{pais}: {len(indicadores)} indicadores")
        print(f"  Indicadores: {', '.join(sorted(indicadores)[:5])}")
        if len(indicadores) > 5:
            print(f"  ... y {len(indicadores) - 5} más")
    
    # Indicadores recomendados para probar
    print("\n" + "=" * 80)
    print("💡 INDICADORES RECOMENDADOS PARA PROBAR:")
    print("=" * 80)
    
    # Buscar indicadores con más países
    indicadores_por_paises = sorted(
        indicadores_paises.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    print("\nTop 10 indicadores con más países disponibles:")
    for i, (indicador, paises) in enumerate(indicadores_por_paises[:10], 1):
        print(f"  {i}. {indicador} ({len(paises)} países)")
        print(f"     Países: {', '.join(sorted(paises.keys())[:5])}")
        if len(paises) > 5:
            print(f"     ... y {len(paises) - 5} más")
    
    print("\n" + "=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    main()

