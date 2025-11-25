-- Script para verificar si las tablas de Brainnova existen en Supabase
-- Ejecuta este script en el SQL Editor de Supabase para verificar

-- Verificar existencia de tablas
SELECT 
    'dimensiones' as tabla,
    CASE WHEN EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'dimensiones') 
         THEN '✅ Existe' 
         ELSE '❌ No existe' 
    END as estado;

SELECT 
    'subdimensiones' as tabla,
    CASE WHEN EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'subdimensiones') 
         THEN '✅ Existe' 
         ELSE '❌ No existe' 
    END as estado;

SELECT 
    'definicion_indicadores' as tabla,
    CASE WHEN EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'definicion_indicadores') 
         THEN '✅ Existe' 
         ELSE '❌ No existe' 
    END as estado;

SELECT 
    'componentes_indicador' as tabla,
    CASE WHEN EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'componentes_indicador') 
         THEN '✅ Existe' 
         ELSE '❌ No existe' 
    END as estado;

SELECT 
    'resultado_indicadores' as tabla,
    CASE WHEN EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'resultado_indicadores') 
         THEN '✅ Existe' 
         ELSE '❌ No existe' 
    END as estado;

SELECT 
    'datos_crudos' as tabla,
    CASE WHEN EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'datos_crudos') 
         THEN '✅ Existe' 
         ELSE '❌ No existe' 
    END as estado;

SELECT 
    'datos_macro' as tabla,
    CASE WHEN EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'datos_macro') 
         THEN '✅ Existe' 
         ELSE '❌ No existe' 
    END as estado;

-- Mostrar estructura de las tablas si existen
SELECT 
    table_name,
    column_name,
    data_type,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name IN ('dimensiones', 'subdimensiones', 'definicion_indicadores', 'componentes_indicador', 'resultado_indicadores', 'datos_crudos', 'datos_macro')
ORDER BY table_name, ordinal_position;

