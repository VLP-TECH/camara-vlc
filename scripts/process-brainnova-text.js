/**
 * Script para procesar el texto del PDF BRAINNOVA y guardarlo en la base de datos
 */

import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = "https://aoykpiievtadhwssugvs.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

function extractKeywords(text) {
  const commonWords = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'si', 'sin', 'sobre', 'este', 'entre', 'cuando', 'todo', 'esta', 'ser', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'años', 'hasta', 'desde', 'está', 'mi', 'porque', 'qué', 'sólo', 'han', 'yo', 'hay', 'vez', 'puede', 'todos', 'así', 'nos', 'ni', 'parte', 'tiene', 'él', 'uno', 'donde', 'bien', 'tiempo', 'mismo', 'ese', 'ahora', 'cada', 'e', 'vida', 'otro', 'después', 'otros', 'aunque'];
  
  const words = text.toLowerCase()
    .replace(/[^\w\sáéíóúñ]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 3 && !commonWords.includes(word));
  
  const wordCount = {};
  words.forEach(word => {
    wordCount[word] = (wordCount[word] || 0) + 1;
  });
  
  return Object.entries(wordCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15)
    .map(([word]) => word);
}

async function saveKnowledgeItem(item) {
  const keywords = extractKeywords(item.content);
  
  const { data, error } = await supabase
    .from('chatbot_knowledge')
    .insert({
      category: item.category,
      title: item.title,
      content: item.content,
      metadata: item.metadata || {},
      source: item.source || 'BRAINNOVA Sistema de Indicadores',
      keywords: keywords
    });
  
  if (error) {
    console.error(`❌ Error guardando: ${item.title.substring(0, 50)} - ${error.message}`);
    return false;
  } else {
    console.log(`✓ Guardado: ${item.title.substring(0, 60)}...`);
    return true;
  }
}

export async function processBrainnovaContent() {
  console.log('📄 Procesando contenido BRAINNOVA...\n');

  const knowledgeItems = [];

  // 1. Información general del sistema
  knowledgeItems.push({
    category: 'general',
    title: 'Sistema BRAINNOVA - Objetivo y descripción general',
    content: `BRAINNOVA es un Sistema de Indicadores de Economía Digital para las empresas de la Comunidad Valenciana. Sus objetivos son:
• Medir el grado de digitalización y transformación digital empresarial en el territorio.
• Establecer un marco de referencia comparable a nivel europeo (usando como base el DESI).
• Incorporar buenas prácticas de marcos internacionales como Going Digital (OCDE), DII (Digital Intensity Index), IMD, NRI, ADB y el Digital Decade Policy Programme.
• Permitir el seguimiento de políticas públicas e inversiones en digitalización.

El sistema implementa una plataforma de visualización interactiva que se convierte en un observatorio activo, capaz de integrar datos de múltiples fuentes y transformarlos en conocimiento accesible.`,
    metadata: { type: 'system_overview' }
  });

  // 2. Dimensiones del sistema
  knowledgeItems.push({
    category: 'kpi',
    title: 'Dimensiones del Sistema BRAINNOVA',
    content: `El sistema BRAINNOVA se organiza en siete dimensiones clave:

1. APOYO AL EMPRENDIMIENTO E INNOVACIÓN (10% del índice global)
   - Acceso a financiación digital
   - Dinamismo emprendedor
   - Infraestructura de apoyo
   - Políticas públicas de fomento

2. CAPITAL HUMANO (20% del índice global)
   - Competencias digitales de la población
   - Formación continua y reciclaje profesional
   - Talento profesional TIC

3. INFRAESTRUCTURA DIGITAL (15% del índice global)
   - Acceso a infraestructuras (banda ancha, 5G, servicios de alta capacidad, nodos Edge)

4. ECOSISTEMA Y COLABORACIÓN (15% del índice global)
   - Conectividad, colaboración y transferencia
   - Entorno de provisión tecnológica

5. TRANSFORMACIÓN DIGITAL EMPRESARIAL (30% del índice global - mayor peso)
   - Digitalización básica
   - E-commerce
   - Tecnologías avanzadas (big data, IA, cloud, RPA, ciberseguridad, ERP, CRM)
   - Cultura organizativa digital

6. SERVICIOS PÚBLICOS DIGITALES (10% del índice global)
   - Disponibilidad de servicios públicos digitales
   - Interacción digital con la administración

7. SOSTENIBILIDAD DIGITAL (5% del índice global)
   - Economía circular y estrategias verdes
   - Eficiencia y huella ambiental`,
    metadata: { type: 'dimensions', weights: { transformation: 30, human_capital: 20, infrastructure: 15, ecosystem: 15, entrepreneurship: 10, public_services: 10, sustainability: 5 } }
  });

  // 3. Metodología
  knowledgeItems.push({
    category: 'general',
    title: 'Metodología BRAINNOVA - Fases de desarrollo',
    content: `La metodología del sistema BRAINNOVA se desarrolla en 5 fases:

FASE 1: Definición conceptual y revisión de marcos de referencia
- Revisión de índices internacionales: DESI, Digital Decade Policy Programme, OECD Going Digital Framework, DII, NRI, IMD World Digital Competitiveness Ranking, Asian Development Bank.

FASE 2: Identificación de indicadores y subdimensiones
- Estructura jerárquica de dimensiones, subdimensiones e indicadores
- Cada indicador incluye: fórmula de cálculo, unidad de medida, fuente de datos, proceso de normalización y marco de referencia europeo o internacional

FASE 3: Captura de información empresarial
- Encuesta específica dirigida a empresas de la Comunidad Valenciana
- Información sobre: estrategia y gobernanza digital, adopción tecnológica, competencias digitales, cultura de innovación, sostenibilidad

FASE 4: Normalización de indicadores
- Transformación a valores relativos y comparables
- Normalización min-max en escala 0-100
- Eliminación de sesgos de escala

FASE 5: Ponderación y construcción del índice compuesto
- Ponderación diferencial basada en relevancia estratégica
- Agregación jerárquica: Indicadores → Subdimensiones → Dimensiones → Índice Global BRAINNOVA`,
    metadata: { type: 'methodology' }
  });

  // 4. Normalización
  knowledgeItems.push({
    category: 'kpi',
    title: 'Proceso de normalización BRAINNOVA',
    content: `El sistema aplica normalización para expresar indicadores en valores comparables:

TIPOS DE VALORES RELATIVOS:
- Indicadores de población: Per cápita (Valor absoluto / Población total)
- Indicadores empresariales: Por empresa activa (Valor absoluto / Número total de empresas)
- Indicadores económicos: Por PIB o GVA (Valor absoluto / PIB regional)
- Indicadores sectoriales: Por empleo en el sector TIC (Valor absoluto / Empleo sectorial)

MÉTODO DE NORMALIZACIÓN:
Fórmula min-max: I_norm = (I - I_min) / (I_max - I_min) × 100

OPCIONES DE REFERENCIA:
1. Top europeo o nacional: I_max = mejor desempeño (análisis de brecha de excelencia)
2. Media europea o nacional: I_max = media (posicionamiento relativo)
3. Objetivo estratégico 2030: I_max = valor objetivo político (evaluación de progreso)

Para indicadores inversos (donde valor alto = negativo), se invierte la escala.`,
    metadata: { type: 'normalization' }
  });

  // 5. Ponderación
  knowledgeItems.push({
    category: 'kpi',
    title: 'Sistema de ponderación BRAINNOVA',
    content: `La ponderación se aplica en tres niveles:

NIVEL 1: Indicadores → Subdimensión
- Media ponderada con pesos: relevancia alta (3), media (2), baja (1)
- Fórmula: S_j = Σ(ω_i × I_norm,i)

NIVEL 2: Subdimensiones → Dimensión
- Media aritmética (todas las subdimensiones contribuyen igual)

NIVEL 3: Dimensiones → Índice Global BRAINNOVA
Ponderación final:
- Transformación digital empresarial: 30% (mayor peso - núcleo del modelo)
- Capital humano: 20% (factor habilitador esencial)
- Infraestructura digital: 15% (habilitador estructural)
- Ecosistema y colaboración: 15% (dinamismo y renovación)
- Apoyo al emprendimiento e innovación: 10% (impacto indirecto)
- Servicios públicos digitales: 10% (impacto periférico)
- Sostenibilidad digital: 5% (dimensión emergente)`,
    metadata: { type: 'weighting', weights: { transformation: 30, human_capital: 20, infrastructure: 15, ecosystem: 15, entrepreneurship: 10, public_services: 10, sustainability: 5 } }
  });

  // 6. Subdimensiones detalladas
  knowledgeItems.push({
    category: 'kpi',
    title: 'Subdimensiones - Apoyo al emprendimiento e innovación',
    content: `DIMENSIÓN: Apoyo al emprendimiento e innovación (10% del índice)

Subdimensiones:
1. Acceso a financiación digital: Analiza la disponibilidad y uso de instrumentos financieros públicos y privados orientados a la digitalización.

2. Dinamismo emprendedor: Mide la creación, densidad y supervivencia de startups digitales.

3. Infraestructura de apoyo: Evalúa la existencia de hubs, aceleradoras y ecosistemas de innovación que impulsan la transformación digital.

4. Políticas públicas de fomento: Cuantifica los programas e inversiones públicas destinadas a la digitalización empresarial.`,
    metadata: { dimension: 'entrepreneurship', weight: 10 }
  });

  knowledgeItems.push({
    category: 'kpi',
    title: 'Subdimensiones - Capital humano',
    content: `DIMENSIÓN: Capital humano (20% del índice)

Subdimensiones:
1. Competencias digitales de la población: Mide la proporción de personas y trabajadores con habilidades digitales básicas y avanzadas.

2. Formación continua y reciclaje profesional: Analiza la formación en TIC dentro de las empresas, el gasto en capacitación y la participación en programas de recualificación digital.

3. Talento profesional TIC: Cuantifica la presencia, movilidad y evolución del empleo en profesiones tecnológicas, así como las dificultades para contratar perfiles especializados.`,
    metadata: { dimension: 'human_capital', weight: 20 }
  });

  knowledgeItems.push({
    category: 'kpi',
    title: 'Subdimensiones - Infraestructura digital',
    content: `DIMENSIÓN: Infraestructura digital (15% del índice)

Subdimensiones:
1. Acceso a infraestructuras: Incluye indicadores sobre:
   - Cobertura de banda ancha
   - Conectividad 5G
   - Adopción de servicios de alta capacidad
   - Despliegue de nodos de datos Edge
   
Evalúa tanto la disponibilidad como el coste relativo de las infraestructuras digitales, elementos clave para la competitividad territorial.`,
    metadata: { dimension: 'infrastructure', weight: 15 }
  });

  knowledgeItems.push({
    category: 'kpi',
    title: 'Subdimensiones - Ecosistema y colaboración',
    content: `DIMENSIÓN: Ecosistema y colaboración (15% del índice)

Subdimensiones:
1. Conectividad, colaboración y transferencia: Evalúa la cooperación entre universidades, centros tecnológicos y empresas, así como la participación en proyectos europeos de innovación.

2. Entorno de provisión tecnológica: Analiza la densidad y el peso económico del sector TIC, la participación en clústeres y redes colaborativas y la interconexión con otros sectores.`,
    metadata: { dimension: 'ecosystem', weight: 15 }
  });

  knowledgeItems.push({
    category: 'kpi',
    title: 'Subdimensiones - Transformación digital empresarial',
    content: `DIMENSIÓN: Transformación digital empresarial (30% del índice - mayor peso)

Subdimensiones:
1. Digitalización básica: Mide la presencia digital de las empresas (sitio web, redes sociales, teletrabajo, uso de herramientas colaborativas).

2. E-commerce: Evalúa la adopción del comercio electrónico, su peso en los ingresos y el grado de internacionalización digital.

3. Tecnologías avanzadas: Incluye la incorporación de:
   - Big data
   - Inteligencia Artificial (IA)
   - Cloud computing
   - RPA (Robotic Process Automation)
   - Ciberseguridad
   - Software de gestión (ERP, CRM)

4. Cultura organizativa digital: Analiza la integración de objetivos digitales en la estrategia, la formación directiva y la apertura al cambio tecnológico.`,
    metadata: { dimension: 'transformation', weight: 30 }
  });

  knowledgeItems.push({
    category: 'kpi',
    title: 'Subdimensiones - Servicios públicos digitales',
    content: `DIMENSIÓN: Servicios públicos digitales (10% del índice)

Subdimensiones:
1. Disponibilidad de servicios públicos digitales: Analiza la digitalización de los trámites administrativos, la inversión TIC pública y el grado de madurez de los servicios digitales.

2. Interacción digital con la administración: Mide el uso de servicios digitales por parte de ciudadanos y empresas, la adopción de sistemas de identidad digital y la satisfacción de los usuarios.`,
    metadata: { dimension: 'public_services', weight: 10 }
  });

  knowledgeItems.push({
    category: 'kpi',
    title: 'Subdimensiones - Sostenibilidad digital',
    content: `DIMENSIÓN: Sostenibilidad digital (5% del índice)

Subdimensiones:
1. Economía circular y estrategias verdes: Mide la inversión y el compromiso empresarial en proyectos de economía circular digital y reducción de emisiones.

2. Eficiencia y huella ambiental: Analiza el uso de TIC para la eficiencia energética, la reducción de papel, la gestión responsable de residuos electrónicos y el consumo energético digital.`,
    metadata: { dimension: 'sustainability', weight: 5 }
  });

  // 7. Encuestas
  knowledgeItems.push({
    category: 'survey',
    title: 'Encuesta empresarial BRAINNOVA',
    content: `El sistema BRAINNOVA incluye una encuesta específica dirigida a empresas de la Comunidad Valenciana para capturar información no observable en fuentes públicas.

La encuesta permite obtener información sobre:
• Estrategia y gobernanza digital
• Adopción tecnológica
• Competencias digitales del personal
• Cultura de innovación y colaboración
• Sostenibilidad y economía circular digital

Las preguntas se estructuran en bloques temáticos alineados con las dimensiones del sistema. Los resultados de la encuesta se integran en el modelo de indicadores mediante procedimientos de normalización y ponderación homogéneos.`,
    metadata: { type: 'survey_info' }
  });

  // 8. Representación visual
  knowledgeItems.push({
    category: 'general',
    title: 'Representación visual del sistema BRAINNOVA',
    content: `El sistema BRAINNOVA incluye representación visual en tres niveles:

NIVEL 1 - Dimensiones estratégicas:
- Radar de dimensiones con las siete dimensiones como ejes principales
- Escala 0-100 (100 = máximo europeo o nacional)
- Permite comparar con media española o valor top europeo

NIVEL 2 - Subdimensiones temáticas:
- Diagramas tipo "árbol" o "mapa de estructura jerárquica"
- Gráficos de barras horizontales o heatmaps
- Panel sintético de indicadores clave con valores actuales, media nacional, top europeo y variación anual

NIVEL 3 - Indicadores operativos:
- Tablas dinámicas y gráficos de barras
- Muestra valor absoluto, normalizado (0-100) y posición relativa
- Incluye explicación del indicador, método de cálculo, origen y fecha

OTRAS VISUALIZACIONES:
- Mapas territoriales: distribución provincial o comarcal
- Evolución temporal: gráficos de líneas o columnas para seguimiento

FUNCIONES ESTRATÉGICAS:
1. Función diagnóstica: identificar áreas fuertes y débiles
2. Función comparativa: posicionar frente a media nacional y europea
3. Función de seguimiento: monitorizar progreso hacia objetivos 2030`,
    metadata: { type: 'visualization' }
  });

  // 9. Índice Global
  knowledgeItems.push({
    category: 'kpi',
    title: 'Índice Global BRAINNOVA',
    content: `El Índice Global BRAINNOVA sintetiza el desempeño digital de la Comunidad Valenciana en una única métrica comparable.

CARACTERÍSTICAS:
- Agrega las siete dimensiones mediante ponderación diferencial
- Expresa valores en términos absolutos y relativos (comparables entre regiones)
- Permite calcular puntuaciones por subdimensión y dimensión
- Actualización anual o bianual según disponibilidad de datos

ESTRUCTURA DE PONDERACIÓN:
- Transformación digital empresarial: 30%
- Capital humano: 20%
- Infraestructura digital: 15%
- Ecosistema y colaboración: 15%
- Apoyo al emprendimiento e innovación: 10%
- Servicios públicos digitales: 10%
- Sostenibilidad digital: 5%

El sistema es escalable y permite incorporar nuevos indicadores o ajustar ponderaciones sin alterar la estructura general.`,
    metadata: { type: 'global_index' }
  });

  // Procesar y guardar todos los items
  console.log(`📦 Procesando ${knowledgeItems.length} items de conocimiento...\n`);
  
  let successCount = 0;
  for (const item of knowledgeItems) {
    const success = await saveKnowledgeItem(item);
    if (success) successCount++;
  }
  
  console.log(`\n✨ Proceso completado!`);
  console.log(`✅ Guardados: ${successCount}/${knowledgeItems.length} items`);
}

// Ejecutar si se llama directamente
if (import.meta.url === `file://${process.argv[1]}`) {
  processBrainnovaContent().catch(console.error);
}

