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
 */
export const getIndicadoresDisponibles = async (): Promise<string[]> => {
  try {
    const response = await fetch(buildUrl('/api/v1/indicadores-disponibles'));
    
    if (!response.ok) {
      await handleApiError(response);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching indicadores:', error);
    // Retornar array vacío si hay error de conexión
    return [];
  }
};

/**
 * Obtiene filtros globales según parámetros
 * GET /api/v1/filtros-globales
 */
export const getFiltrosGlobales = async (params?: {
  nombre_indicador?: string;
  pais?: string;
  periodo?: number;
  sector?: string;
  tamano?: string;
}): Promise<FiltrosGlobalesResponse> => {
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
    const response = await fetch(url);
    
    if (!response.ok) {
      await handleApiError(response);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching filtros globales:', error);
    // Retornar objeto vacío si hay error de conexión
    return {
      paises: [],
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
    const response = await fetch(url);
    
    if (!response.ok) {
      await handleApiError(response);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching resultados:', error);
    // Retornar array vacío si hay error de conexión
    return [];
  }
};

/**
 * Calcula el Brainnova Score
 * POST /api/v1/brainnova-score
 */
export const calculateBrainnovaScore = async (
  data: BrainnovaScoreRequest
): Promise<BrainnovaScoreResponse> => {
  const response = await fetch(buildUrl('/api/v1/brainnova-score'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    await handleApiError(response);
  }
  
  return response.json();
};

