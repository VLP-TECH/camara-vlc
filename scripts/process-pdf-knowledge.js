/**
 * Script para procesar PDF y extraer información para el chatbot
 * 
 * Uso: node scripts/process-pdf-knowledge.js <ruta-al-pdf>
 */

import { createClient } from '@supabase/supabase-js';
import fs from 'fs';
import path from 'path';

const SUPABASE_URL = "https://aoykpiievtadhwssugvs.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFveWtwaWlldnRhZGh3c3N1Z3ZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYyMDkyMzksImV4cCI6MjA3MTc4NTIzOX0.8XoaRingLHPyGtuHgtfHnkVF6SDP8u64nrdOco9v4JY";

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Esta función será reemplazada cuando agreguemos pdf-parse
async function extractTextFromPDF(pdfPath) {
  // Por ahora, retornamos un placeholder
  // Cuando instales pdf-parse, descomenta el código de abajo
  /*
  const pdfParse = await import('pdf-parse');
  const dataBuffer = fs.readFileSync(pdfPath);
  const data = await pdfParse.default(dataBuffer);
  return data.text;
  */
  
  throw new Error('Por favor instala pdf-parse: npm install pdf-parse');
}

function extractKeywords(text) {
  // Extrae palabras clave relevantes del texto
  const commonWords = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'una', 'como', 'más', 'pero', 'sus', 'le', 'ha', 'me', 'si', 'sin', 'sobre', 'este', 'entre', 'cuando', 'todo', 'esta', 'ser', 'son', 'dos', 'también', 'fue', 'había', 'era', 'muy', 'años', 'hasta', 'desde', 'está', 'mi', 'porque', 'qué', 'sólo', 'han', 'yo', 'hay', 'vez', 'puede', 'todos', 'así', 'nos', 'ni', 'parte', 'tiene', 'él', 'uno', 'donde', 'bien', 'tiempo', 'mismo', 'ese', 'ahora', 'cada', 'e', 'vida', 'otro', 'después', 'te', 'otros', 'aunque', 'esas', 'esos', 'esas', 'esos', 'esas', 'esos'];
  
  const words = text.toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 3 && !commonWords.includes(word));
  
  // Retorna las palabras más frecuentes (top 10)
  const wordCount = {};
  words.forEach(word => {
    wordCount[word] = (wordCount[word] || 0) + 1;
  });
  
  return Object.entries(wordCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([word]) => word);
}

function parseContent(text) {
  // Intenta identificar KPIs, encuestas, y otra información estructurada
  const sections = [];
  
  // Buscar secciones de KPIs (números, porcentajes, valores)
  const kpiPattern = /([A-ZÁÉÍÓÚÑ][^.!?]*?)(\d+[.,]?\d*%?|\d+[.,]?\d*\s*(millones|miles|euros|€|%))/gi;
  const kpiMatches = [...text.matchAll(kpiPattern)];
  
  kpiMatches.forEach(match => {
    sections.push({
      category: 'kpi',
      title: match[1].trim().substring(0, 100),
      content: match[0].trim(),
      metadata: { value: match[2] }
    });
  });
  
  // Buscar secciones sobre encuestas
  const surveyPattern = /(encuesta|survey|cuestionario)[^.!?]*?[.!?]/gi;
  const surveyMatches = [...text.matchAll(surveyPattern)];
  
  surveyMatches.forEach(match => {
    sections.push({
      category: 'survey',
      title: 'Información sobre encuestas',
      content: match[0].trim()
    });
  });
  
  // Si no hay secciones específicas, dividir por párrafos
  if (sections.length === 0) {
    const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim().length > 50);
    paragraphs.forEach((para, idx) => {
      const firstLine = para.split('\n')[0].substring(0, 100);
      sections.push({
        category: 'general',
        title: firstLine || `Sección ${idx + 1}`,
        content: para.trim()
      });
    });
  }
  
  return sections;
}

async function processPDF(pdfPath) {
  console.log(`📄 Procesando PDF: ${pdfPath}`);
  
  if (!fs.existsSync(pdfPath)) {
    throw new Error(`El archivo no existe: ${pdfPath}`);
  }
  
  // Extraer texto del PDF
  console.log('📖 Extrayendo texto del PDF...');
  const text = await extractTextFromPDF(pdfPath);
  
  // Parsear contenido
  console.log('🔍 Analizando contenido...');
  const sections = parseContent(text);
  
  console.log(`✅ Encontradas ${sections.length} secciones`);
  
  // Guardar en base de datos
  console.log('💾 Guardando en base de datos...');
  const fileName = path.basename(pdfPath);
  
  for (const section of sections) {
    const keywords = extractKeywords(section.content);
    
    const { data, error } = await supabase
      .from('chatbot_knowledge')
      .insert({
        category: section.category,
        title: section.title,
        content: section.content,
        metadata: section.metadata || {},
        source: fileName,
        keywords: keywords
      });
    
    if (error) {
      console.error(`❌ Error guardando sección: ${error.message}`);
    } else {
      console.log(`✓ Guardado: ${section.title.substring(0, 50)}...`);
    }
  }
  
  console.log('✨ Proceso completado!');
}

// Ejecutar si se llama directamente
const pdfPath = process.argv[2];
if (pdfPath) {
  processPDF(pdfPath).catch(console.error);
} else {
  console.log('Uso: node scripts/process-pdf-knowledge.js <ruta-al-pdf>');
}

