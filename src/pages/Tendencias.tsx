import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import NavigationHeader from "@/components/NavigationHeader";
import FooterSection from "@/components/FooterSection";
import { TrendingUp, Loader2, AlertCircle } from "lucide-react";
import { toast } from "@/hooks/use-toast";
import {
  getIndicadoresDisponibles,
  getFiltrosGlobales,
  getResultados,
} from "@/lib/brainnova-api";

const Tendencias = () => {
  const [indicadorSeleccionado, setIndicadorSeleccionado] = useState<string>("");
  const [paisSeleccionado, setPaisSeleccionado] = useState<string>("");
  const [provinciaSeleccionada, setProvinciaSeleccionada] = useState<string>("");
  const [sectorSeleccionado, setSectorSeleccionado] = useState<string>("");

  // Cargar indicadores disponibles
  const {
    data: indicadores,
    isLoading: loadingIndicadores,
    error: errorIndicadores,
  } = useQuery({
    queryKey: ["indicadores-disponibles"],
    queryFn: getIndicadoresDisponibles,
    retry: 1,
    retryDelay: 1000,
  });

  // Cargar filtros globales según indicador seleccionado
  const {
    data: filtrosPorIndicador,
    isLoading: loadingFiltrosIndicador,
  } = useQuery({
    queryKey: ["filtros-globales", "indicador", indicadorSeleccionado],
    queryFn: () =>
      getFiltrosGlobales({
        nombre_indicador: indicadorSeleccionado,
      }),
    enabled: !!indicadorSeleccionado,
    retry: 1,
    retryDelay: 1000,
  });

  // Cargar filtros globales según indicador y país
  const {
    data: filtrosPorPais,
    isLoading: loadingFiltrosPais,
  } = useQuery({
    queryKey: ["filtros-globales", "pais", indicadorSeleccionado, paisSeleccionado],
    queryFn: () =>
      getFiltrosGlobales({
        nombre_indicador: indicadorSeleccionado,
        pais: paisSeleccionado,
      }),
    enabled: !!indicadorSeleccionado && !!paisSeleccionado,
    retry: 1,
    retryDelay: 1000,
  });

  // Cargar resultados para el gráfico
  const {
    data: resultados,
    isLoading: loadingResultados,
    error: errorResultados,
  } = useQuery({
    queryKey: [
      "resultados",
      indicadorSeleccionado,
      paisSeleccionado,
      provinciaSeleccionada,
      sectorSeleccionado,
    ],
    queryFn: () =>
      getResultados({
        nombre_indicador: indicadorSeleccionado,
        pais: paisSeleccionado,
        provincia: provinciaSeleccionada || undefined,
        sector: sectorSeleccionado || undefined,
      }),
    enabled:
      !!indicadorSeleccionado &&
      !!paisSeleccionado,
    retry: 1,
    retryDelay: 1000,
  });

  // Auto-seleccionar país si solo hay uno disponible
  useEffect(() => {
    if (
      filtrosPorIndicador?.paises &&
      filtrosPorIndicador.paises.length === 1 &&
      !paisSeleccionado
    ) {
      setPaisSeleccionado(filtrosPorIndicador.paises[0]);
    }
  }, [filtrosPorIndicador, paisSeleccionado]);

  // Resetear selecciones cuando cambia el indicador
  useEffect(() => {
    if (indicadorSeleccionado) {
      setPaisSeleccionado("");
      setProvinciaSeleccionada("");
      setSectorSeleccionado("");
    }
  }, [indicadorSeleccionado]);

  // Resetear provincia y sector cuando cambia el país
  useEffect(() => {
    if (paisSeleccionado) {
      setProvinciaSeleccionada("");
      setSectorSeleccionado("");
    }
  }, [paisSeleccionado]);

  // Manejar errores
  useEffect(() => {
    if (errorIndicadores) {
      toast({
        title: "Error",
        description: "No se pudieron cargar los indicadores disponibles",
        variant: "destructive",
      });
    }
    if (errorResultados) {
      toast({
        title: "Error",
        description: "No se pudieron cargar los resultados",
        variant: "destructive",
      });
    }
  }, [errorIndicadores, errorResultados]);

  // Preparar datos para el gráfico
  const datosGrafico = resultados?.map((item) => ({
    periodo: item.periodo,
    valor: item.valor,
  })) || [];

  return (
    <div className="min-h-screen bg-background">
      <NavigationHeader />

      <main className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-12 text-center">
            <h1 className="text-4xl font-bold text-foreground mb-4 flex items-center justify-center gap-2">
              <TrendingUp className="h-8 w-8 text-primary" />
              Gráfico de tendencias
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Visualiza la evolución histórica de los indicadores del ecosistema digital
            </p>
          </div>

          {/* Filtros */}
          <Card className="p-6 mb-8 bg-gradient-card border-0">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Selector de Indicador */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Indicador
                </label>
                <Select
                  value={indicadorSeleccionado}
                  onValueChange={setIndicadorSeleccionado}
                  disabled={loadingIndicadores}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona un indicador" />
                  </SelectTrigger>
                  <SelectContent>
                    {indicadores?.map((indicador) => (
                      <SelectItem key={indicador} value={indicador}>
                        {indicador}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Selector de País */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  País
                </label>
                <Select
                  value={paisSeleccionado}
                  onValueChange={setPaisSeleccionado}
                  disabled={
                    !indicadorSeleccionado ||
                    loadingFiltrosIndicador ||
                    !filtrosPorIndicador?.paises?.length
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona un país" />
                  </SelectTrigger>
                  <SelectContent>
                    {filtrosPorIndicador?.paises?.map((pais) => (
                      <SelectItem key={pais} value={pais}>
                        {pais}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Selector de Provincia */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Provincia
                </label>
                <Select
                  value={provinciaSeleccionada}
                  onValueChange={setProvinciaSeleccionada}
                  disabled={
                    !paisSeleccionado ||
                    loadingFiltrosPais ||
                    !filtrosPorPais?.provincias?.length
                  }
                >
                  <SelectTrigger>
                    <SelectValue
                      placeholder={
                        filtrosPorPais?.provincias?.length
                          ? "Selecciona una provincia"
                          : "(Nacional)"
                      }
                    />
                  </SelectTrigger>
                  <SelectContent>
                    {filtrosPorPais?.provincias?.map((provincia) => (
                      <SelectItem key={provincia} value={provincia}>
                        {provincia}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Selector de Sector */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Sector
                </label>
                <Select
                  value={sectorSeleccionado}
                  onValueChange={setSectorSeleccionado}
                  disabled={
                    !paisSeleccionado ||
                    loadingFiltrosPais ||
                    !filtrosPorPais?.sectores?.length
                  }
                >
                  <SelectTrigger>
                    <SelectValue
                      placeholder={
                        filtrosPorPais?.sectores?.length
                          ? "Selecciona un sector"
                          : "(No aplica / Todos)"
                      }
                    />
                  </SelectTrigger>
                  <SelectContent>
                    {filtrosPorPais?.sectores?.map((sector) => (
                      <SelectItem key={sector} value={sector}>
                        {sector}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </Card>

          {/* Gráfico */}
          <Card className="p-6 bg-gradient-card border-0">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-foreground flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-primary" />
                Evolución histórica
              </h3>
            </div>

            {loadingResultados ? (
              <div className="flex items-center justify-center h-96">
                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
              </div>
            ) : errorResultados ? (
              <div className="flex flex-col items-center justify-center h-96">
                <AlertCircle className="h-12 w-12 text-destructive mb-4" />
                <p className="text-muted-foreground">
                  No se pudieron cargar los datos
                </p>
              </div>
            ) : datosGrafico.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-96">
                <AlertCircle className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">
                  {indicadorSeleccionado && paisSeleccionado
                    ? "No hay datos disponibles para los filtros seleccionados"
                    : "Selecciona un indicador y un país para ver el gráfico"}
                </p>
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={datosGrafico}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                  <XAxis
                    dataKey="periodo"
                    stroke="hsl(var(--muted-foreground))"
                  />
                  <YAxis stroke="hsl(var(--muted-foreground))" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="valor"
                    stroke="hsl(var(--primary))"
                    strokeWidth={2}
                    name="Valor"
                    dot={{ fill: "hsl(var(--primary))" }}
                  />
                </LineChart>
              </ResponsiveContainer>
            )}
          </Card>
        </div>
      </main>

      <FooterSection />
    </div>
  );
};

export default Tendencias;

