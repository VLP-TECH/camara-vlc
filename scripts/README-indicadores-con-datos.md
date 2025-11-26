# Cómo encontrar indicadores con datos para probar el gráfico de Tendencias

## Opción 1: Usar el SQL Editor de Supabase (Recomendado)

1. Ve a tu proyecto en Supabase
2. Abre el **SQL Editor**
3. Ejecuta el siguiente query:

```sql
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
```

Esto te mostrará los 10 mejores indicadores con datos para España.

## Opción 2: Usar la consola del navegador

1. Abre la página `/tendencias` en tu navegador
2. Abre la consola del desarrollador (F12 o Cmd+Option+I)
3. Pega y ejecuta este código:

```javascript
async function checkIndicadores() {
  const { supabase } = await import('/src/integrations/supabase/client.ts');
  
  const { data, error } = await supabase
    .from('resultado_indicadores')
    .select('nombre_indicador, pais, periodo')
    .eq('pais', 'España')
    .order('periodo', { ascending: false })
    .limit(500);

  if (error) {
    console.error('Error:', error);
    return;
  }

  const indicadoresMap = new Map();
  
  data.forEach((r) => {
    const nombre = r.nombre_indicador || '';
    if (!nombre) return;
    
    if (!indicadoresMap.has(nombre)) {
      indicadoresMap.set(nombre, {
        nombre,
        periodos: new Set(),
        totalResultados: 0,
      });
    }
    
    const ind = indicadoresMap.get(nombre);
    if (r.periodo) ind.periodos.add(r.periodo);
    ind.totalResultados++;
  });

  const indicadores = Array.from(indicadoresMap.values())
    .filter(ind => ind.totalResultados >= 5)
    .sort((a, b) => b.periodos.size - a.periodos.size)
    .slice(0, 10);

  console.log('\n=== ✅ INDICADORES RECOMENDADOS PARA PROBAR ===\n');
  indicadores.forEach((ind, i) => {
    const periodos = Array.from(ind.periodos).sort((a, b) => a - b);
    console.log(`${i + 1}. "${ind.nombre}"`);
    console.log(`   - Total de datos: ${ind.totalResultados}`);
    console.log(`   - Períodos: ${periodos[0]} - ${periodos[periodos.length - 1]} (${ind.periodos.size} períodos)`);
    console.log('');
  });
}

checkIndicadores();
```

## Opción 3: Verificar directamente en la página

La página de Tendencias ahora tiene un fallback automático a Supabase, por lo que:

1. Los indicadores que aparecen en el selector **ya tienen datos disponibles**
2. Si seleccionas un indicador y un país, el gráfico debería mostrar datos automáticamente
3. Si no aparecen datos, puede ser que:
   - El indicador no tenga datos para ese país específico
   - Los datos estén en formato provincial (prueba seleccionando una provincia)
   - El indicador no tenga suficientes períodos para mostrar una tendencia

## Ejemplos de indicadores que suelen tener datos

Basado en la estructura típica de datos de Brainnova, estos indicadores suelen tener datos:

- **Uso regular de Internet**
- **Empresas que usan inteligencia artificial**
- **Porcentaje de empresas con página web**
- **Personas con competencias digitales básicas**
- **Uso de servicios en la nube**
- **Ventas online**

## Notas importantes

- El gráfico necesita al menos **3-5 puntos de datos** para mostrar una tendencia clara
- Algunos indicadores pueden tener datos solo para ciertos países
- Si el backend no está disponible, la página usará automáticamente los datos de Supabase

