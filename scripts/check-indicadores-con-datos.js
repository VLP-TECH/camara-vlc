// Script para verificar qué indicadores tienen datos disponibles
// Ejecutar en la consola del navegador en la página de Tendencias

async function checkIndicadoresConDatos() {
  try {
    const { supabase } = await import('/src/integrations/supabase/client.ts');
    
    // Obtener todos los indicadores que tienen resultados
    const { data: resultados, error } = await supabase
      .from('resultado_indicadores')
      .select('nombre_indicador, pais, provincia, periodo, valor_calculado')
      .order('periodo', { ascending: false })
      .limit(1000);

    if (error) {
      console.error('Error:', error);
      return;
    }

    if (!resultados || resultados.length === 0) {
      console.log('❌ No hay resultados en la base de datos');
      return;
    }

    // Agrupar por indicador
    const indicadoresMap = new Map();

    resultados.forEach((r) => {
      const nombre = r.nombre_indicador || '';
      if (!nombre) return;

      if (!indicadoresMap.has(nombre)) {
        indicadoresMap.set(nombre, {
          nombre,
          paises: new Set(),
          periodos: new Set(),
          totalResultados: 0,
          ultimoPeriodo: 0,
          ejemploValor: 0,
        });
      }

      const indicador = indicadoresMap.get(nombre);
      if (r.pais) indicador.paises.add(r.pais);
      if (r.periodo) indicador.periodos.add(r.periodo);
      indicador.totalResultados++;
      if (r.periodo && r.periodo > indicador.ultimoPeriodo) {
        indicador.ultimoPeriodo = r.periodo;
        indicador.ejemploValor = Number(r.valor_calculado) || 0;
      }
    });

    // Convertir a array y ordenar por total de resultados
    const indicadores = Array.from(indicadoresMap.values())
      .sort((a, b) => b.totalResultados - a.totalResultados);

    console.log('\n=== 📊 INDICADORES CON DATOS DISPONIBLES ===\n');
    console.log(`Total de indicadores con datos: ${indicadores.length}\n`);

    indicadores.slice(0, 20).forEach((ind, index) => {
      const periodos = Array.from(ind.periodos).sort((a, b) => b - a);
      const paises = Array.from(ind.paises);
      
      console.log(`${index + 1}. ${ind.nombre}`);
      console.log(`   📊 Total resultados: ${ind.totalResultados}`);
      console.log(`   🌍 Países: ${paises.join(', ') || 'N/A'}`);
      console.log(`   📅 Períodos: ${periodos.slice(0, 5).join(', ')}${periodos.length > 5 ? '...' : ''} (${periodos.length} períodos)`);
      console.log(`   📈 Último período: ${ind.ultimoPeriodo} (valor: ${ind.ejemploValor.toFixed(2)})`);
      console.log('');
    });

    // Mostrar los mejores para probar
    console.log('\n=== ✅ RECOMENDACIONES PARA PROBAR ===\n');
    const mejores = indicadores
      .filter(ind => ind.paises.has('España') && ind.totalResultados >= 5)
      .slice(0, 5);
    
    if (mejores.length > 0) {
      mejores.forEach((ind, index) => {
        console.log(`${index + 1}. "${ind.nombre}"`);
        console.log(`   - País: España`);
        console.log(`   - Total de datos: ${ind.totalResultados}`);
        console.log(`   - Último período: ${ind.ultimoPeriodo}`);
        console.log('');
      });
    } else {
      console.log('No se encontraron indicadores con suficientes datos para España.');
      console.log('Prueba con otros países o verifica que los datos estén cargados.');
    }

  } catch (error) {
    console.error('Error:', error);
  }
}

// Ejecutar la función
checkIndicadoresConDatos();

