import { supabase } from "@/integrations/supabase/client";

export interface KnowledgeItem {
  id: string;
  category: string;
  title: string;
  content: string;
  metadata?: any;
  source?: string;
  keywords?: string[];
}

/**
 * Busca información relevante en la base de datos del chatbot
 */
export async function searchKnowledge(query: string, category?: string): Promise<KnowledgeItem[]> {
  try {
    // Limpiar la consulta: eliminar signos de interrogación y caracteres especiales
    const cleanQuery = query.replace(/[¿?¡!]/g, '').trim();
    
    // Palabras comunes a excluir
    const stopWords = ['son', 'las', 'los', 'del', 'de', 'la', 'el', 'en', 'un', 'una', 'que', 'con', 'por', 'para', 'cuáles', 'cuál', 'qué', 'cómo', 'cuándo', 'dónde'];
    
    const searchTerms = cleanQuery.toLowerCase()
      .split(/\s+/)
      .filter(term => term.length > 2 && !stopWords.includes(term));
    
    if (searchTerms.length === 0) {
      return [];
    }
    
    let queryBuilder = supabase
      .from('chatbot_knowledge')
      .select('*');
    
    if (category) {
      queryBuilder = queryBuilder.eq('category', category);
    }
    
    // Construir condiciones de búsqueda - priorizar términos más largos y específicos
    // Ordenar términos por longitud (más largos primero) para mejor matching
    const sortedTerms = [...searchTerms].sort((a, b) => b.length - a.length);
    const conditions = sortedTerms.map(term => `title.ilike.%${term}%,content.ilike.%${term}%`).join(',');
    
    // Buscar en título y contenido
    const { data, error } = await queryBuilder
      .or(conditions)
      .order('created_at', { ascending: false })
      .limit(10);
    
    if (error) {
      console.error('Error searching knowledge:', error);
      // Intentar búsqueda alternativa más simple
      const { data: altData, error: altError } = await supabase
        .from('chatbot_knowledge')
        .select('*')
        .ilike('title', `%${searchTerms[0]}%`)
        .limit(10);
      
      if (altError) {
        console.error('Alternative search also failed:', altError);
        return [];
      }
      
      const altResults = (altData || []).map(item => ({
        ...item,
        relevance: calculateRelevance(item, searchTerms)
      })).sort((a, b) => b.relevance - a.relevance);
      
      return altResults;
    }
    
    // Ordenar por relevancia (más coincidencias = más relevante)
    const results = (data || []).map(item => ({
      ...item,
      relevance: calculateRelevance(item, searchTerms)
    })).sort((a, b) => b.relevance - a.relevance);
    
    return results;
  } catch (error) {
    console.error('Error in searchKnowledge:', error);
    return [];
  }
}

/**
 * Calcula la relevancia de un resultado basado en los términos de búsqueda
 */
function calculateRelevance(item: KnowledgeItem, searchTerms: string[]): number {
  let score = 0;
  const titleLower = item.title.toLowerCase();
  const contentLower = item.content.toLowerCase();
  const keywordsLower = (item.keywords || []).map(k => k.toLowerCase());
  
  searchTerms.forEach(term => {
    // Título tiene más peso
    if (titleLower.includes(term)) score += 3;
    // Keywords tienen peso medio
    if (keywordsLower.some(k => k.includes(term))) score += 2;
    // Contenido tiene peso bajo
    if (contentLower.includes(term)) score += 1;
  });
  
  return score;
}

/**
 * Obtiene información sobre encuestas disponibles
 */
export async function getSurveyInfo(): Promise<any[]> {
  try {
    const { data, error } = await supabase
      .from('surveys')
      .select('id, title, description, active')
      .eq('active', true);
    
    if (error) {
      console.error('Error fetching surveys:', error);
      return [];
    }
    
    return data || [];
  } catch (error) {
    console.error('Error in getSurveyInfo:', error);
    return [];
  }
}

/**
 * Obtiene información sobre KPIs
 */
export async function getKPIInfo(): Promise<KnowledgeItem[]> {
  return searchKnowledge('kpi indicador métrica', 'kpi');
}

/**
 * Genera una respuesta del chatbot basada en la consulta del usuario
 */
export async function generateChatbotResponse(userQuery: string): Promise<string> {
  // Limpiar la consulta
  const cleanQuery = userQuery.replace(/[¿?¡!]/g, '').trim();
  const lowerQuery = cleanQuery.toLowerCase();
  
  // Detectar si pregunta sobre encuestas
  if (lowerQuery.includes('encuesta') || lowerQuery.includes('survey') || lowerQuery.includes('cuestionario')) {
    const surveys = await getSurveyInfo();
    if (surveys.length > 0) {
      const surveyList = surveys.map(s => `• ${s.title}: ${s.description || 'Sin descripción'}`).join('\n');
      return `Encontré ${surveys.length} encuesta(s) disponible(s):\n\n${surveyList}\n\n¿Sobre cuál te gustaría saber más?`;
    } else {
      return 'No hay encuestas activas en este momento.';
    }
  }
  
  // Detectar si pregunta sobre KPIs
  if (lowerQuery.includes('kpi') || lowerQuery.includes('indicador') || lowerQuery.includes('métrica') || lowerQuery.includes('dato')) {
    const kpiInfo = await getKPIInfo();
    if (kpiInfo.length > 0) {
      const kpiDetails = kpiInfo.slice(0, 3).map(k => `• ${k.title}: ${k.content.substring(0, 150)}...`).join('\n\n');
      return `Información sobre KPIs e indicadores:\n\n${kpiDetails}\n\n¿Quieres más detalles sobre algún indicador específico?`;
    }
  }
  
  // Búsqueda general en la base de conocimiento
  const results = await searchKnowledge(cleanQuery);
  
  if (results.length > 0) {
    // Priorizar resultados más específicos (que contengan más términos de búsqueda en el título)
    const searchTerms = lowerQuery.split(/\s+/).filter(term => term.length > 2);
    const sortedResults = results.sort((a, b) => {
      const aTitleMatches = searchTerms.filter(term => a.title.toLowerCase().includes(term)).length;
      const bTitleMatches = searchTerms.filter(term => b.title.toLowerCase().includes(term)).length;
      if (aTitleMatches !== bTitleMatches) return bTitleMatches - aTitleMatches;
      return b.relevance - a.relevance;
    });
    
    const bestMatch = sortedResults[0];
    let response = bestMatch.content;
    
    // Si hay más resultados relevantes, mencionarlos
    if (sortedResults.length > 1 && sortedResults[1].relevance > 2) {
      response += `\n\nTambién encontré información relacionada sobre "${sortedResults[1].title}". ¿Te interesa?`;
    }
    
    return response;
  }
  
  // Si no encuentra nada, intentar búsquedas más amplias
  const keyTerms = lowerQuery.split(/\s+/).filter(term => term.length > 3);
  if (keyTerms.length > 0) {
    // Intentar buscar solo con el término más importante
    const broadResults = await searchKnowledge(keyTerms[0]);
    if (broadResults.length > 0) {
      return broadResults[0].content;
    }
  }
  
  // Respuesta por defecto si no encuentra nada
  return `No encontré información específica sobre "${cleanQuery}" en la base de conocimiento. ¿Podrías reformular tu pregunta o ser más específico? Puedo ayudarte con información sobre encuestas, KPIs, indicadores y datos del ecosistema digital valenciano.`;
}

