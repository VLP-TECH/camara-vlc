// Funciones para obtener datos del dashboard desde Supabase
import { supabase } from "@/integrations/supabase/client";

export interface DashboardStats {
  totalIndicadores: number;
  totalDimensiones: number;
  totalSubdimensiones: number;
  totalResultados: number;
  totalDatosCrudos: number;
}

export interface DimensionStats {
  nombre: string;
  peso: number;
  indicadoresCount: number;
  subdimensionesCount: number;
}

export interface IndicatorTrend {
  nombre: string;
  valores: Array<{
    periodo: number;
    valor: number;
  }>;
}

/**
 * Obtiene estadísticas generales del dashboard
 */
export async function getDashboardStats(): Promise<DashboardStats> {
  try {
    const [indicadores, dimensiones, subdimensiones, resultados, datosCrudos] = await Promise.all([
      supabase.from("definicion_indicadores").select("nombre", { count: "exact", head: true }),
      supabase.from("dimensiones").select("nombre", { count: "exact", head: true }),
      supabase.from("subdimensiones").select("nombre", { count: "exact", head: true }),
      supabase.from("resultado_indicadores").select("id", { count: "exact", head: true }),
      supabase.from("datos_crudos").select("id", { count: "exact", head: true }),
    ]);

    return {
      totalIndicadores: indicadores.count || 0,
      totalDimensiones: dimensiones.count || 0,
      totalSubdimensiones: subdimensiones.count || 0,
      totalResultados: resultados.count || 0,
      totalDatosCrudos: datosCrudos.count || 0,
    };
  } catch (error) {
    console.error("Error fetching dashboard stats:", error);
    return {
      totalIndicadores: 0,
      totalDimensiones: 0,
      totalSubdimensiones: 0,
      totalResultados: 0,
      totalDatosCrudos: 0,
    };
  }
}

/**
 * Obtiene estadísticas por dimensión
 */
export async function getDimensionStats(): Promise<DimensionStats[]> {
  try {
    const { data: dimensiones, error } = await supabase
      .from("dimensiones")
      .select("nombre, peso")
      .order("peso", { ascending: false });

    if (error) throw error;

    const stats = await Promise.all(
      (dimensiones || []).map(async (dim) => {
        // Obtener subdimensiones de esta dimensión
        const { data: subdimensiones } = await supabase
          .from("subdimensiones")
          .select("nombre")
          .eq("nombre_dimension", dim.nombre);

        // Contar indicadores de todas las subdimensiones
        let indicadoresCount = 0;
        if (subdimensiones && subdimensiones.length > 0) {
          const counts = await Promise.all(
            subdimensiones.map((sub) =>
              supabase
                .from("definicion_indicadores")
                .select("nombre", { count: "exact", head: true })
                .eq("nombre_subdimension", sub.nombre)
            )
          );
          indicadoresCount = counts.reduce((sum, c) => sum + (c.count || 0), 0);
        }

        return {
          nombre: dim.nombre,
          peso: dim.peso,
          indicadoresCount,
          subdimensionesCount: subdimensiones?.length || 0,
        };
      })
    );

    return stats;
  } catch (error) {
    console.error("Error fetching dimension stats:", error);
    return [];
  }
}

/**
 * Obtiene los últimos valores de indicadores para mostrar en KPIs
 */
export async function getLatestIndicatorValues(pais: string = "España", periodo?: number): Promise<Array<{
  nombre: string;
  valor: number;
  periodo: number;
}>> {
  try {
    let query = supabase
      .from("resultado_indicadores")
      .select("nombre_indicador, valor_calculado, periodo")
      .eq("pais", pais)
      .order("periodo", { ascending: false })
      .limit(100);

    if (periodo) {
      query = query.eq("periodo", periodo);
    }

    const { data, error } = await query;

    if (error) throw error;

    // Agrupar por indicador y tomar el valor más reciente
    const latestValues = new Map<string, { nombre: string; valor: number; periodo: number }>();

    (data || []).forEach((item) => {
      const key = item.nombre_indicador;
      const existing = latestValues.get(key);
      
      if (!existing || item.periodo > existing.periodo) {
        latestValues.set(key, {
          nombre: item.nombre_indicador || "",
          valor: Number(item.valor_calculado) || 0,
          periodo: item.periodo || 0,
        });
      }
    });

    return Array.from(latestValues.values());
  } catch (error) {
    console.error("Error fetching latest indicator values:", error);
    return [];
  }
}

/**
 * Obtiene tendencias de un indicador específico
 */
export async function getIndicatorTrend(
  nombreIndicador: string,
  pais: string = "España",
  limit: number = 10
): Promise<IndicatorTrend | null> {
  try {
    const { data, error } = await supabase
      .from("resultado_indicadores")
      .select("periodo, valor_calculado")
      .eq("nombre_indicador", nombreIndicador)
      .eq("pais", pais)
      .order("periodo", { ascending: true })
      .limit(limit);

    if (error) throw error;

    if (!data || data.length === 0) return null;

    return {
      nombre: nombreIndicador,
      valores: data.map((item) => ({
        periodo: item.periodo || 0,
        valor: Number(item.valor_calculado) || 0,
      })),
    };
  } catch (error) {
    console.error("Error fetching indicator trend:", error);
    return null;
  }
}

/**
 * Obtiene los indicadores más importantes (por importancia)
 */
export async function getTopIndicators(limit: number = 10): Promise<Array<{
  nombre: string;
  importancia: string;
  dimension: string;
  subdimension: string;
}>> {
  try {
    const { data: indicadores, error } = await supabase
      .from("definicion_indicadores")
      .select("nombre, importancia, nombre_subdimension")
      .in("importancia", ["Alta", "EXTRAIDO"])
      .limit(limit);

    if (error) throw error;

    // Obtener dimensiones para cada indicador
    const indicadoresConDimension = await Promise.all(
      (indicadores || []).map(async (ind) => {
        const { data: subdim } = await supabase
          .from("subdimensiones")
          .select("nombre_dimension")
          .eq("nombre", ind.nombre_subdimension)
          .single();

        return {
          nombre: ind.nombre,
          importancia: ind.importancia || "Media",
          dimension: subdim?.nombre_dimension || "",
          subdimension: ind.nombre_subdimension,
        };
      })
    );

    return indicadoresConDimension;
  } catch (error) {
    console.error("Error fetching top indicators:", error);
    return [];
  }
}

