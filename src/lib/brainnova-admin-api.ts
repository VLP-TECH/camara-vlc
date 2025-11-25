// Servicio de API para gestión administrativa de Brainnova
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
 * Obtiene estadísticas de la base de datos
 */
export const getDatabaseStats = async () => {
  try {
    const response = await fetch(buildUrl('/api/v1/admin/stats'));
    
    if (!response.ok) {
      await handleApiError(response);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching database stats:', error);
    // Retornar objeto con valores por defecto si hay error
    return {
      total_indicadores: 0,
      total_resultados: 0,
      total_datos_crudos: 0,
      total_datos_macro: 0
    };
  }
};

/**
 * Inicia el proceso de ingesta de datos
 */
export const triggerIngesta = async () => {
  const response = await fetch(buildUrl('/api/v1/admin/ingesta'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  if (!response.ok) {
    await handleApiError(response);
  }
  
  return response.json();
};

/**
 * Obtiene el estado del proceso de ingesta
 */
export const getIngestaStatus = async () => {
  try {
    const response = await fetch(buildUrl('/api/v1/admin/ingesta/status'));
    
    if (!response.ok) {
      await handleApiError(response);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching ingesta status:', error);
    // Retornar estado por defecto si hay error
    return {
      status: 'inactive',
      last_run: null
    };
  }
};

/**
 * Obtiene el log del proceso de ingesta
 */
export const getIngestaLog = async (limit: number = 100) => {
  try {
    const response = await fetch(buildUrl(`/api/v1/admin/ingesta/log?limit=${limit}`));
    
    if (!response.ok) {
      await handleApiError(response);
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching ingesta log:', error);
    // Retornar array vacío si hay error
    return [];
  }
};

