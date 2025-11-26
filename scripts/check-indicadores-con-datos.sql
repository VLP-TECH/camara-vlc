-- Script SQL para verificar qué indicadores tienen datos en la base de datos
-- Ejecutar este script en el SQL Editor de Supabase

-- Obtener indicadores con datos, agrupados por nombre
SELECT 
  nombre_indicador,
  COUNT(*) as total_resultados,
  COUNT(DISTINCT pais) as total_paises,
  COUNT(DISTINCT periodo) as total_periodos,
  MIN(periodo) as primer_periodo,
  MAX(periodo) as ultimo_periodo,
  STRING_AGG(DISTINCT pais, ', ' ORDER BY pais) as paises_disponibles,
  AVG(valor_calculado) as valor_promedio
FROM resultado_indicadores
WHERE nombre_indicador IS NOT NULL
GROUP BY nombre_indicador
HAVING COUNT(*) >= 3  -- Al menos 3 resultados para tener una tendencia
ORDER BY total_resultados DESC, ultimo_periodo DESC
LIMIT 30;

-- Obtener los mejores indicadores para España (para probar el gráfico)
SELECT 
  nombre_indicador,
  COUNT(*) as total_resultados,
  COUNT(DISTINCT periodo) as total_periodos,
  MIN(periodo) as primer_periodo,
  MAX(periodo) as ultimo_periodo,
  AVG(valor_calculado) as valor_promedio
FROM resultado_indicadores
WHERE nombre_indicador IS NOT NULL
  AND pais = 'España'
  AND (provincia IS NULL OR provincia = '')
GROUP BY nombre_indicador
HAVING COUNT(*) >= 5  -- Al menos 5 resultados para tener una buena tendencia
ORDER BY total_periodos DESC, ultimo_periodo DESC
LIMIT 10;

