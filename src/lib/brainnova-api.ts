// Servicio de API para Brainnova Backend
import type {
  FiltrosGlobalesResponse,
  ResultadosResponse,
  BrainnovaScoreRequest,
  BrainnovaScoreResponse,
} from './brainnova-types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Construye la URL completa para un endpoint
 */
const buildUrl = (endpoint: string): string => {
  return `${API_BASE_URL}${endpoint}`;
};

/**
 * Maneja errores de la API
 */
const handleApiError = async (response: Response): Promise<never> => {
  let errorMessage = `Error ${response.status}: ${response.statusText}`;
  try {
    const errorData = await response.json();
    errorMessage = errorData.detail || errorData.message || errorMessage;
  } catch {
    // Si no se puede parsear el JSON, usar el mensaje por defecto
  }
  throw new Error(errorMessage);
};

/**
 * Obtiene la lista de indicadores disponibles
 * GET /api/v1/indicadores-disponibles
 * Fallback a Supabase si el backend no está disponible
 */
export const getIndicadoresDisponibles = async (): Promise<string[]> => {
  try {
    const response = await fetch(buildUrl('/api/v1/indicadores-disponibles'), {
      signal: AbortSignal.timeout(5000), // Timeout de 5 segundos
    });
    
    // Si el backend devuelve un error (500, 404, etc.), usar fallback a Supabase
    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }
    
    let data;
    try {
      data = await response.json();
    } catch (jsonError) {
      // Si no se puede parsear el JSON, usar fallback
      throw new Error('Backend returned invalid JSON');
    }
    
    // Si el backend devuelve datos, usarlos
    if (Array.isArray(data) && data.length > 0) {
      return data;
    }
    
    // Si el backend devuelve array vacío, intentar desde Supabase
    throw new Error('Backend returned empty data');
  } catch (error) {
    console.warn('Error fetching indicadores from backend, trying Supabase fallback:', error);
    
    // Fallback: obtener indicadores desde Supabase
    try {
      const supabaseModule = await import('@/integrations/supabase/client');
      const supabase = supabaseModule.supabase;
      
      // Obtener todos los indicadores definidos
      const { data: definiciones, error: errorDefiniciones } = await supabase
        .from('definicion_indicadores')
        .select('nombre');
      
      if (errorDefiniciones) {
        console.error('Error fetching definiciones from Supabase:', errorDefiniciones);
        // Fallback: obtener desde resultado_indicadores
        const { data: resultados } = await supabase
          .from('resultado_indicadores')
          .select('nombre_indicador')
          .not('nombre_indicador', 'is', null);
        
        if (!resultados || resultados.length === 0) {
          return [];
        }
        
        const indicadores = Array.from(
          new Set(resultados.map(item => item.nombre_indicador).filter(Boolean))
        ).sort();
        
        return indicadores;
      }
      
      if (!definiciones || definiciones.length === 0) {
        return [];
      }
      
      // Normalizar nombres (eliminar duplicados por capitalización)
      const indicadoresNormalizados = new Map<string, string>();
      for (const def of definiciones) {
        const nombre = def.nombre?.trim();
        if (!nombre) continue;
        
        const normalizado = nombre.toLowerCase().trim();
        if (!indicadoresNormalizados.has(normalizado)) {
          indicadoresNormalizados.set(normalizado, nombre);
        } else {
          // Si hay duplicado, mantener la versión más completa
          const existente = indicadoresNormalizados.get(normalizado);
          if (nombre.length > existente.length) {
            indicadoresNormalizados.set(normalizado, nombre);
          }
        }
      }
      
      // Ordenar alfabéticamente
      const indicadores = Array.from(indicadoresNormalizados.values()).sort();
      
      return indicadores;
    } catch (supabaseError) {
      console.error('Error in Supabase fallback:', supabaseError);
      return [];
    }
  }
};

/**
 * Obtiene filtros globales según parámetros
 * GET /api/v1/filtros-globales
 * Fallback a Supabase si el backend no está disponible
 */
export const getFiltrosGlobales = async (params?: {
  nombre_indicador?: string;
  pais?: string;
  periodo?: number;
  sector?: string;
  tamano?: string;
}): Promise<FiltrosGlobalesResponse> => {
  // Intentar backend primero con timeout corto
  try {
    const queryParams = new URLSearchParams();
    
    if (params?.nombre_indicador) {
      queryParams.append('nombre_indicador', params.nombre_indicador);
    }
    if (params?.pais) {
      queryParams.append('pais', params.pais);
    }
    if (params?.periodo) {
      queryParams.append('periodo', params.periodo.toString());
    }
    if (params?.sector) {
      queryParams.append('sector', params.sector);
    }
    if (params?.tamano) {
      queryParams.append('tamano', params.tamano);
    }
    
    const url = buildUrl(`/api/v1/filtros-globales${queryParams.toString() ? `?${queryParams.toString()}` : ''}`);
    const response = await fetch(url, {
      signal: AbortSignal.timeout(3000), // Timeout corto de 3 segundos
    });
    
    // Si el backend devuelve un error (500, 404, etc.), usar fallback a Supabase
    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }
    
    let data;
    try {
      data = await response.json();
    } catch (jsonError) {
      // Si no se puede parsear el JSON, usar fallback
      throw new Error('Backend returned invalid JSON');
    }
    
    // Si el backend devuelve datos válidos, usarlos
    if (data && (data.paises?.length > 0 || data.anios?.length > 0 || data.provincias?.length > 0)) {
      return data;
    }
    
    // Si el backend devuelve datos vacíos, intentar desde Supabase
    throw new Error('Backend returned empty data');
  } catch (error) {
    // Siempre usar fallback a Supabase si el backend falla
    console.warn('Backend no disponible, usando Supabase:', error);
  }
  
  // Fallback: obtener filtros desde Supabase
  try {
    const supabaseModule = await import('@/integrations/supabase/client');
    const supabase = supabaseModule.supabase;
    
    if (!supabase) {
      throw new Error('No se pudo cargar el cliente de Supabase');
    }
    
    // Construir query base
    let query = supabase
      .from('resultado_indicadores')
      .select('pais, provincia, periodo, nombre_indicador');
    
    // Aplicar filtros según parámetros
    if (params?.nombre_indicador) {
      // Buscar por nombre de indicador (puede haber variaciones de capitalización)
      query = query.ilike('nombre_indicador', `%${params.nombre_indicador}%`);
    }
    if (params?.pais) {
      query = query.eq('pais', params.pais);
    }
    if (params?.periodo) {
      query = query.eq('periodo', params.periodo);
    }
    
    const { data, error: supabaseError } = await query;
    
    if (supabaseError) {
      console.error('Error en Supabase:', supabaseError);
      // Si hay error, devolver todos los países disponibles (sin filtrar por indicador)
      const { data: todosPaises } = await supabase
        .from('resultado_indicadores')
        .select('pais');
      
      if (todosPaises && todosPaises.length > 0) {
        const paisesUnicos = Array.from(new Set(todosPaises.map(item => item.pais).filter(Boolean))).sort();
        return {
          paises: paisesUnicos,
          provincias: [],
          sectores: [],
          tamanos_empresa: [],
          anios: []
        };
      }
      
      return {
        paises: [],
        provincias: [],
        sectores: [],
        tamanos_empresa: [],
        anios: []
      };
    }
    
    if (!data || data.length === 0) {
      // Si no hay datos para el indicador específico, devolver todos los países disponibles
      const { data: todosPaises } = await supabase
        .from('resultado_indicadores')
        .select('pais');
      
      if (todosPaises && todosPaises.length > 0) {
        const paisesUnicos = Array.from(new Set(todosPaises.map(item => item.pais).filter(Boolean))).sort();
        return {
          paises: paisesUnicos,
          provincias: [],
          sectores: [],
          tamanos_empresa: [],
          anios: []
        };
      }
      
      return {
        paises: [],
        provincias: [],
        sectores: [],
        tamanos_empresa: [],
        anios: []
      };
    }
    
    // Extraer valores únicos
    const paises = Array.from(new Set(data.map(item => item.pais).filter(Boolean))).sort();
    const provincias = Array.from(new Set(data.map(item => item.provincia).filter(Boolean))).sort();
    const anios = Array.from(new Set(data.map(item => item.periodo).filter(Boolean))).sort((a, b) => b - a);
    
    return {
      paises: paises.length > 0 ? paises : ['España'], // Si no hay países, devolver España por defecto
      provincias,
      sectores: [], // No hay columna sector en la tabla actual
      tamanos_empresa: [], // No hay columna tamano_empresa en la tabla actual
      anios
    };
  } catch (supabaseError) {
    console.error('Error en fallback de Supabase:', supabaseError);
    // Devolver al menos España como opción por defecto
    return {
      paises: ['España'],
      provincias: [],
      sectores: [],
      tamanos_empresa: [],
      anios: []
    };
  }
};

/**
 * Obtiene resultados históricos para el gráfico
 * GET /api/v1/resultados
 * Fallback a Supabase si el backend no está disponible
 */
export const getResultados = async (params: {
  nombre_indicador: string;
  pais: string;
  sector?: string;
  provincia?: string;
}): Promise<ResultadosResponse[]> => {
  try {
    const queryParams = new URLSearchParams();
    queryParams.append('nombre_indicador', params.nombre_indicador);
    queryParams.append('pais', params.pais);
    
    if (params.sector) {
      queryParams.append('sector', params.sector);
    }
    if (params.provincia) {
      queryParams.append('provincia', params.provincia);
    }
    
    const url = buildUrl(`/api/v1/resultados?${queryParams.toString()}`);
    const response = await fetch(url, {
      signal: AbortSignal.timeout(5000), // Timeout de 5 segundos
    });
    
    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Si el backend devuelve datos, usarlos
    if (Array.isArray(data) && data.length > 0) {
      return data;
    }
    
    // Si el backend devuelve array vacío, intentar desde Supabase
    throw new Error('Backend returned empty data');
  } catch (error) {
    console.warn('Error fetching resultados from backend, trying Supabase fallback:', error);
    
    // Fallback: obtener datos directamente desde Supabase
    try {
      const supabaseModule = await import('@/integrations/supabase/client');
      const supabase = supabaseModule.supabase;
      
      let query = supabase
        .from('resultado_indicadores')
        .select('periodo, valor_calculado, pais, provincia, sector')
        .eq('nombre_indicador', params.nombre_indicador)
        .eq('pais', params.pais)
        .order('periodo', { ascending: true });
      
      if (params.provincia) {
        query = query.eq('provincia', params.provincia);
      } else {
        // Si no se especifica provincia, obtener datos nacionales (provincia null o vacía)
        query = query.or('provincia.is.null,provincia.eq.');
      }
      
      if (params.sector) {
        query = query.eq('sector', params.sector);
      }
      
      const { data, error: supabaseError } = await query;
      
      if (supabaseError) {
        console.error('Error fetching from Supabase:', supabaseError);
        return [];
      }
      
      if (!data || data.length === 0) {
        return [];
      }
      
      // Mapear datos de Supabase al formato esperado
      return data.map((item) => ({
        periodo: item.periodo,
        valor: typeof item.valor_calculado === 'number' 
          ? item.valor_calculado 
          : parseFloat(String(item.valor_calculado || 0)) || 0,
      }));
    } catch (supabaseError) {
      console.error('Error in Supabase fallback:', supabaseError);
      return [];
    }
  }
};

/**
 * Calcula el Brainnova Score
 * POST /api/v1/brainnova-score
 * Fallback a Supabase si el backend no está disponible
 */
export const calculateBrainnovaScore = async (
  data: BrainnovaScoreRequest
): Promise<BrainnovaScoreResponse> => {
  try {
    const response = await fetch(buildUrl('/api/v1/brainnova-score'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      signal: AbortSignal.timeout(10000), // Timeout de 10 segundos para cálculos
    });
    
    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }
    
    const result = await response.json();
    
    // Si el backend devuelve datos válidos, usarlos
    if (result && (result.brainnova_global_score !== undefined || result.indice_ponderado !== undefined)) {
      // Normalizar formato de respuesta
      return {
        indice_ponderado: result.brainnova_global_score || result.indice_ponderado,
        desglose: result.desglose_por_dimension?.reduce((acc: any, dim: any) => {
          acc[dim.dimension] = dim.score_dimension;
          return acc;
        }, {}) || result.desglose,
        ...result
      };
    }
    
    throw new Error('Backend returned invalid data');
  } catch (error) {
    console.warn('Error calculating Brainnova score from backend, trying Supabase fallback:', error);
    
    // Fallback: calcular score desde Supabase
    try {
      const supabaseModule = await import('@/integrations/supabase/client');
      const supabase = supabaseModule.supabase;
      
      // Mapa de importancia
      const MAPA_IMPORTANCIA: { [key: string]: number } = {
        "Alta": 3, "Media": 2, "Baja": 1,
        "alta": 3, "media": 2, "baja": 1
      };
      
      // 1. Obtener resultados de indicadores
      let query = supabase
        .from('resultado_indicadores')
        .select('valor_calculado, nombre_indicador')
        .eq('pais', data.pais)
        .eq('periodo', data.periodo);
      
      if (data.provincia) {
        query = query.eq('provincia', data.provincia);
      } else {
        // Si no hay provincia, obtener datos nacionales (provincia null o vacía)
        query = query.or('provincia.is.null,provincia.eq.');
      }
      
      if (data.sector) {
        query = query.eq('sector', data.sector);
      }
      // Si no hay sector, no aplicamos filtro (obtener todos)
      
      if (data.tamano_empresa) {
        query = query.eq('tamano_empresa', data.tamano_empresa);
      }
      // Si no hay tamaño, no aplicamos filtro (obtener todos)
      
      const { data: resultados, error: supabaseError } = await query;
      
      if (supabaseError) {
        console.error('Error fetching from Supabase:', supabaseError);
        throw new Error('No se pudieron obtener los datos necesarios para calcular el score');
      }
      
      if (!resultados || resultados.length === 0) {
        throw new Error('No hay datos suficientes para calcular el score con los filtros seleccionados');
      }
      
      // 2. Obtener información de indicadores, subdimensiones y dimensiones
      const nombresIndicadores = Array.from(new Set(resultados.map(r => r.nombre_indicador).filter(Boolean)));
      
      // Obtener definiciones de indicadores
      const { data: definiciones } = await supabase
        .from('definicion_indicadores')
        .select('nombre, importancia, nombre_subdimension')
        .in('nombre', nombresIndicadores);
      
      if (!definiciones || definiciones.length === 0) {
        throw new Error('No se encontraron definiciones para los indicadores');
      }
      
      // Obtener subdimensiones
      const nombresSubdimensiones = Array.from(new Set(definiciones.map(d => d.nombre_subdimension).filter(Boolean)));
      const { data: subdimensiones } = await supabase
        .from('subdimensiones')
        .select('nombre, nombre_dimension')
        .in('nombre', nombresSubdimensiones);
      
      if (!subdimensiones || subdimensiones.length === 0) {
        throw new Error('No se encontraron subdimensiones');
      }
      
      // Obtener dimensiones
      const nombresDimensiones = Array.from(new Set(subdimensiones.map(s => s.nombre_dimension).filter(Boolean)));
      const { data: dimensiones } = await supabase
        .from('dimensiones')
        .select('nombre, peso')
        .in('nombre', nombresDimensiones);
      
      if (!dimensiones || dimensiones.length === 0) {
        throw new Error('No se encontraron dimensiones');
      }
      
      // Crear mapas para acceso rápido
      const mapIndicadorSubdim = new Map(definiciones.map(d => [d.nombre, d.nombre_subdimension]));
      const mapIndicadorImportancia = new Map(definiciones.map(d => [d.nombre, d.importancia || "Baja"]));
      const mapSubdimDim = new Map(subdimensiones.map(s => [s.nombre, s.nombre_dimension]));
      const mapDimPeso = new Map(dimensiones.map(d => [d.nombre, d.peso || 0]));
      
      // 3. Procesar datos: agrupar por dimensión y subdimensión
      type TreeStructure = {
        [dimId: string]: {
          [subdimId: string]: Array<{ val: number; w: number }>;
        };
      };
      
      const tree: TreeStructure = {};
      const dimInfo: { [key: string]: { nombre: string; peso_pct: number } } = {};
      
      for (const row of resultados) {
        const nombreIndicador = row.nombre_indicador;
        if (!nombreIndicador) continue;
        
        const valor = parseFloat(String(row.valor_calculado || 0));
        const importancia = mapIndicadorImportancia.get(nombreIndicador) || "Baja";
        const peso = MAPA_IMPORTANCIA[importancia] || 1;
        
        const nombreSubdim = mapIndicadorSubdim.get(nombreIndicador);
        if (!nombreSubdim) continue;
        
        const nombreDim = mapSubdimDim.get(nombreSubdim);
        if (!nombreDim) continue;
        
        const dimPeso = mapDimPeso.get(nombreDim) || 0;
        
        if (!tree[nombreDim]) {
          tree[nombreDim] = {};
          dimInfo[nombreDim] = { nombre: nombreDim, peso_pct: dimPeso };
        }
        
        if (!tree[nombreDim][nombreSubdim]) {
          tree[nombreDim][nombreSubdim] = [];
        }
        
        tree[nombreDim][nombreSubdim].push({ val: valor, w: peso });
      }
      
      // 4. Calcular scores por dimensión (Nivel 1 y 2)
      const scoresDimensiones: { [key: string]: number } = {};
      
      for (const [dimNombre, subdims] of Object.entries(tree)) {
        const subdimVals: number[] = [];
        
        for (const [subdimNombre, inds] of Object.entries(subdims)) {
          // Media ponderada por importancia (Nivel 1)
          const num = inds.reduce((sum, i) => sum + i.val * i.w, 0);
          const den = inds.reduce((sum, i) => sum + i.w, 0);
          const subdimScore = den > 0 ? num / den : 0;
          subdimVals.push(subdimScore);
        }
        
        // Media aritmética de subdimensiones (Nivel 2)
        scoresDimensiones[dimNombre] = subdimVals.length > 0
          ? subdimVals.reduce((sum, val) => sum + val, 0) / subdimVals.length
          : 0;
      }
      
      // 5. Calcular score global (Nivel 3)
      let brainnovaScore = 0;
      const desglose: { [key: string]: number } = {};
      
      for (const [dimNombre, score] of Object.entries(scoresDimensiones)) {
        const info = dimInfo[dimNombre];
        if (!info) continue;
        
        const contrib = score * (info.peso_pct / 100.0);
        brainnovaScore += contrib;
        desglose[dimNombre] = Math.round(score * 100) / 100;
      }
      
      return {
        indice_ponderado: Math.round(brainnovaScore * 100) / 100,
        desglose,
        brainnova_global_score: Math.round(brainnovaScore * 100) / 100,
        pais: data.pais,
        periodo: data.periodo,
        sector: data.sector,
        tamano_empresa: data.tamano_empresa,
        provincia: data.provincia
      };
    } catch (supabaseError) {
      console.error('Error in Supabase fallback for Brainnova score:', supabaseError);
      throw supabaseError instanceof Error 
        ? supabaseError 
        : new Error('No se pudo calcular el Brainnova score. Verifica que haya datos disponibles para los filtros seleccionados.');
    }
  }
};

