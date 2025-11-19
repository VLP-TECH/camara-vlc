/**
 * Script para ejecutar SQL directamente en Supabase usando la API
 */

import { createClient } from '@supabase/supabase-js';
import fs from 'fs';

const SUPABASE_URL = "https://aoykpiievtadhwssugvs.supabase.co";
// Necesitamos la service_role_key para ejecutar SQL, pero por seguridad usaremos anon
// y ejecutaremos desde el dashboard o con service_role si está disponible
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function executeSQL(sqlFile) {
  console.log(`📄 Leyendo archivo SQL: ${sqlFile}`);
  const sql = fs.readFileSync(sqlFile, 'utf8');
  
  // Dividir en statements individuales
  const statements = sql
    .split(';')
    .map(s => s.trim())
    .filter(s => s.length > 0 && !s.startsWith('--'));
  
  console.log(`📦 Encontrados ${statements.length} statements SQL\n`);
  
  // Ejecutar cada statement
  for (let i = 0; i < statements.length; i++) {
    const statement = statements[i];
    if (statement.length < 10) continue; // Skip very short statements
    
    console.log(`⏳ Ejecutando statement ${i + 1}/${statements.length}...`);
    
    try {
      // Usar rpc para ejecutar SQL (requiere función específica)
      // Alternativamente, podemos usar la API REST directamente
      const { data, error } = await supabase.rpc('exec_sql', { sql_query: statement });
      
      if (error) {
        // Si no existe la función rpc, intentar método alternativo
        console.log(`⚠️  No se puede ejecutar directamente. Por favor ejecuta el SQL manualmente en el dashboard.`);
        console.log(`\n📋 SQL a ejecutar:\n${sql}\n`);
        return false;
      }
      
      console.log(`✓ Statement ${i + 1} ejecutado`);
    } catch (err) {
      console.error(`❌ Error en statement ${i + 1}:`, err.message);
      console.log(`\n⚠️  No se puede ejecutar SQL directamente desde aquí.`);
      console.log(`\n📋 Por favor, ejecuta el siguiente SQL en el dashboard de Supabase:`);
      console.log(`\n${sql}\n`);
      return false;
    }
  }
  
  return true;
}

// Ejecutar
const sqlFile = process.argv[2] || 'scripts/setup-chatbot-db.sql';
executeSQL(sqlFile).catch(console.error);

