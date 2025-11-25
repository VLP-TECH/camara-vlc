/**
 * Script para cargar datos de Brainnova en Supabase
 * Lee los datos del backend y los inserta en Supabase
 */

import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';
import { parse } from 'csv-parse/sync';

// Configuración de Supabase
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || "https://aoykpiievtadhwssugvs.supabase.co";
const SUPABASE_SERVICE_KEY = import.meta.env.VITE_SUPABASE_SERVICE_ROLE_KEY || "";

if (!SUPABASE_SERVICE_KEY) {
  console.error("❌ Error: VITE_SUPABASE_SERVICE_ROLE_KEY no está configurado");
  console.log("Necesitas configurar la clave de servicio de Supabase para poder insertar datos.");
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

// Estructura de datos según el backend
interface DimensionData {
  nombre: string;
  peso: number;
  subdimensiones: SubdimensionData[];
}

interface SubdimensionData {
  nombre: string;
  peso: number;
  indicadores: IndicadorData[];
}

interface IndicadorData {
  nombre: string;
  nombre_subdimension: string;
  importancia: string;
  formula: string;
  fuente: string;
  origen_indicador: string;
  componentes?: ComponenteData[];
}

interface ComponenteData {
  descripcion_dato: string;
  fuente_tabla: string;
}

// Datos de dimensiones según setup.py del backend
const DATOS_ESG: Record<string, { peso: number; subdimensiones: Array<{ nombre: string; peso: number }> }> = {
  "Emprendimiento e innovación": {
    peso: 10,
    subdimensiones: [
      { nombre: "Acceso a financiación", peso: 0 },
      { nombre: "Dinamismo emprendedor", peso: 0 },
      { nombre: "Infraestructura de apoyo", peso: 0 },
      { nombre: "Políticas de fomento", peso: 0 }
    ]
  },
  "Capital humano": {
    peso: 20,
    subdimensiones: [
      { nombre: "Competencias digitales", peso: 0 },
      { nombre: "Formación continua", peso: 0 },
      { nombre: "Talento profesional", peso: 0 }
    ]
  },
  "Ecosistema y colaboración": {
    peso: 15,
    subdimensiones: [
      { nombre: "Atractivo del ecosistema", peso: 0 },
      { nombre: "Provision tecnológica", peso: 0 },
      { nombre: "Transferencia de conocimiento", peso: 0 }
    ]
  },
  "Infraestructura digital": {
    peso: 15,
    subdimensiones: [
      { nombre: "Acceso a infraestructuras", peso: 0 }
    ]
  },
  "Servicios públicos digitales": {
    peso: 10,
    subdimensiones: [
      { nombre: "Disponibilidad de servicios digitales", peso: 0 },
      { nombre: "Integración con administración", peso: 0 }
    ]
  },
  "Sostenibilidad digital": {
    peso: 5,
    subdimensiones: [
      { nombre: "Economía circular", peso: 0 },
      { nombre: "Huella ambiental", peso: 0 }
    ]
  },
  "Transformación digital empresarial": {
    peso: 30,
    subdimensiones: [
      { nombre: "Organización digital", peso: 0 },
      { nombre: "Digitalización básica", peso: 0 },
      { nombre: "E-commerce", peso: 0 },
      { nombre: "Tecnologías avanzadas", peso: 0 }
    ]
  }
};

/**
 * Carga las dimensiones en Supabase
 */
async function loadDimensiones(): Promise<void> {
  console.log("📊 Cargando dimensiones...");
  
  const dimensiones = Object.keys(DATOS_ESG).map(nombre => ({
    nombre,
    peso: DATOS_ESG[nombre].peso
  }));

  const { error } = await supabase
    .from('dimensiones')
    .upsert(dimensiones, { onConflict: 'nombre' });

  if (error) {
    console.error("❌ Error cargando dimensiones:", error);
    throw error;
  }

  console.log(`✅ ${dimensiones.length} dimensiones cargadas`);
}

/**
 * Carga las subdimensiones en Supabase
 */
async function loadSubdimensiones(): Promise<void> {
  console.log("📊 Cargando subdimensiones...");
  
  const subdimensiones: Array<{ nombre: string; nombre_dimension: string; peso: number }> = [];
  
  for (const [nombreDim, datos] of Object.entries(DATOS_ESG)) {
    for (const subdim of datos.subdimensiones) {
      subdimensiones.push({
        nombre: subdim.nombre,
        nombre_dimension: nombreDim,
        peso: subdim.peso
      });
    }
  }

  const { error } = await supabase
    .from('subdimensiones')
    .upsert(subdimensiones, { onConflict: 'nombre' });

  if (error) {
    console.error("❌ Error cargando subdimensiones:", error);
    throw error;
  }

  console.log(`✅ ${subdimensiones.length} subdimensiones cargadas`);
}

/**
 * Lee el archivo Excel/CSV de indicadores y los carga
 * Por ahora, creamos un script que se puede ejecutar desde el backend Python
 */
async function loadIndicadores(): Promise<void> {
  console.log("📊 Cargando indicadores...");
  console.log("⚠️  Nota: Los indicadores deben cargarse desde el backend Python");
  console.log("    Ejecuta el script de Python que procesa el Excel de indicadores");
}

/**
 * Carga datos crudos desde archivos CSV procesados
 */
async function loadDatosCrudos(csvPath: string): Promise<void> {
  console.log(`📊 Cargando datos crudos desde ${csvPath}...`);
  
  if (!fs.existsSync(csvPath)) {
    console.warn(`⚠️  Archivo no encontrado: ${csvPath}`);
    return;
  }

  const csvContent = fs.readFileSync(csvPath, 'utf-8');
  const records = parse(csvContent, {
    columns: true,
    skip_empty_lines: true,
    bom: true
  });

  // Mapear los datos según la estructura esperada
  const datosCrudos = records.map((record: any) => ({
    nombre_indicador: record.nombre_indicador || null,
    valor: parseFloat(record.valor) || null,
    unidad: record.unidad || null,
    pais: record.pais || null,
    provincia: record.provincia || null,
    periodo: parseInt(record.periodo) || null,
    descripcion_dato: record.descripcion_dato || null
  })).filter((d: any) => d.valor !== null && d.periodo !== null);

  if (datosCrudos.length > 0) {
    const { error } = await supabase
      .from('datos_crudos')
      .insert(datosCrudos);

    if (error) {
      console.error("❌ Error cargando datos crudos:", error);
      throw error;
    }

    console.log(`✅ ${datosCrudos.length} registros de datos crudos cargados`);
  }
}

/**
 * Carga datos macro desde archivos CSV procesados
 */
async function loadDatosMacro(csvPath: string): Promise<void> {
  console.log(`📊 Cargando datos macro desde ${csvPath}...`);
  
  if (!fs.existsSync(csvPath)) {
    console.warn(`⚠️  Archivo no encontrado: ${csvPath}`);
    return;
  }

  const csvContent = fs.readFileSync(csvPath, 'utf-8');
  const records = parse(csvContent, {
    columns: true,
    skip_empty_lines: true,
    bom: true
  });

  const datosMacro = records.map((record: any) => ({
    valor: parseFloat(record.valor) || null,
    unidad: record.unidad || null,
    pais: record.pais || null,
    provincia: record.provincia || null,
    periodo: parseInt(record.periodo) || null,
    descripcion_dato: record.descripcion_dato || null
  })).filter((d: any) => d.valor !== null && d.periodo !== null);

  if (datosMacro.length > 0) {
    const { error } = await supabase
      .from('datos_macro')
      .insert(datosMacro);

    if (error) {
      console.error("❌ Error cargando datos macro:", error);
      throw error;
    }

    console.log(`✅ ${datosMacro.length} registros de datos macro cargados`);
  }
}

/**
 * Función principal
 */
async function main() {
  console.log("🚀 Iniciando carga de datos en Supabase...\n");

  try {
    // 1. Cargar dimensiones
    await loadDimensiones();
    
    // 2. Cargar subdimensiones
    await loadSubdimensiones();
    
    // 3. Cargar indicadores (nota: debe hacerse desde el backend Python)
    await loadIndicadores();
    
    console.log("\n✅ Carga de datos completada");
    console.log("\n📝 Próximos pasos:");
    console.log("   1. Ejecuta el script de Python del backend para cargar indicadores");
    console.log("   2. Usa loadDatosCrudos() y loadDatosMacro() para cargar datos procesados");
    
  } catch (error) {
    console.error("\n❌ Error durante la carga:", error);
    process.exit(1);
  }
}

// Ejecutar si se llama directamente
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { loadDimensiones, loadSubdimensiones, loadIndicadores, loadDatosCrudos, loadDatosMacro };

