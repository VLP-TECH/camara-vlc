/**
 * Script que intenta crear la tabla y cargar los datos
 * Si no puede crear la tabla, muestra instrucciones
 */

import { createClient } from '@supabase/supabase-js';
import fs from 'fs';

const SUPABASE_URL = "https://aoykpiievtadhwssugvs.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function checkTableExists() {
  try {
    const { data, error } = await supabase
      .from('chatbot_knowledge')
      .select('id')
      .limit(1);
    
    if (error && error.code === '42P01') {
      // Table doesn't exist
      return false;
    }
    return !error;
  } catch (err) {
    return false;
  }
}

async function loadBrainnovaData() {
  console.log('📄 Cargando datos de BRAINNOVA...\n');
  
  // Ejecutar el script de procesamiento directamente
  const processModule = await import('./process-brainnova-text.js');
  
  try {
    // La función ya está exportada, solo necesitamos ejecutarla
    await processModule.processBrainnovaContent();
    console.log('\n✅ Datos cargados exitosamente!');
  } catch (error) {
    console.error('\n❌ Error cargando datos:', error.message);
    throw error;
  }
}

async function main() {
  console.log('🔍 Verificando si la tabla existe...\n');
  
  const tableExists = await checkTableExists();
  
  if (!tableExists) {
    console.log('❌ La tabla chatbot_knowledge no existe.\n');
    console.log('📋 Por favor, ejecuta el siguiente SQL en el SQL Editor de Supabase:\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    
    const sqlContent = fs.readFileSync('scripts/setup-chatbot-db.sql', 'utf8');
    console.log(sqlContent);
    
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log('📍 URL del SQL Editor: https://supabase.com/dashboard/project/aoykpiievtadhwssugvs/sql/new\n');
    console.log('⏳ Después de ejecutar el SQL, vuelve a ejecutar este script para cargar los datos.\n');
    process.exit(1);
  }
  
  console.log('✅ La tabla existe. Cargando datos...\n');
  await loadBrainnovaData();
}

main().catch(console.error);

