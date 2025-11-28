// Script para probar conexión a Supabase y verificar datos
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  'https://aoykpiievtadhwssugvs.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY'
);

async function testSupabase() {
  console.log('🔍 Verificando datos en Supabase...\n');
  
  // 1. Verificar resultados
  console.log('1️⃣ Consultando resultado_indicadores...');
  const { data: resultados, error: errorResultados } = await supabase
    .from('resultado_indicadores')
    .select('pais, periodo, nombre_indicador')
    .limit(5);
  
  if (errorResultados) {
    console.log('❌ Error:', errorResultados.message);
  } else {
    console.log('✅ Resultados encontrados:', resultados?.length);
    console.log('📊 Muestra:', JSON.stringify(resultados, null, 2));
  }
  
  // 2. Verificar países únicos
  console.log('\n2️⃣ Consultando países únicos...');
  const { data: paises, error: errorPaises } = await supabase
    .from('resultado_indicadores')
    .select('pais');
  
  if (errorPaises) {
    console.log('❌ Error:', errorPaises.message);
  } else {
    const paisesUnicos = [...new Set(paises?.map(p => p.pais))];
    console.log('✅ Países encontrados:', paisesUnicos);
  }
  
  // 3. Verificar indicadores
  console.log('\n3️⃣ Consultando indicadores...');
  const { data: indicadores, error: errorIndicadores } = await supabase
    .from('definicion_indicadores')
    .select('nombre');
  
  if (errorIndicadores) {
    console.log('❌ Error:', errorIndicadores.message);
  } else {
    console.log('✅ Indicadores definidos:', indicadores?.length);
    console.log('📋 Lista:', indicadores?.map(i => i.nombre).slice(0, 5));
  }
  
  // 4. Verificar dimensiones
  console.log('\n4️⃣ Consultando dimensiones...');
  const { data: dimensiones, error: errorDimensiones } = await supabase
    .from('dimensiones')
    .select('nombre');
  
  if (errorDimensiones) {
    console.log('❌ Error:', errorDimensiones.message);
  } else {
    console.log('✅ Dimensiones:', dimensiones?.map(d => d.nombre));
  }
}

testSupabase().catch(console.error);

