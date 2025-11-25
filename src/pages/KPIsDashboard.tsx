import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import NavigationHeader from "@/components/NavigationHeader";
import FooterSection from "@/components/FooterSection";
import { 
  TrendingUp, 
  Lightbulb, 
  GraduationCap, 
  Users, 
  Wifi, 
  Building2, 
  Leaf, 
  Briefcase,
  Download,
  ArrowUpRight,
  Loader2,
  Database
} from "lucide-react";
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis
} from "recharts";
import {
  getDimensiones,
  getIndicadoresConDatos,
  getDatosHistoricosIndicador,
  getDatosPorSubdimension,
  type IndicadorConDatos,
} from "@/lib/kpis-data";
import {
  exportIndicadoresToCSV,
  exportChartDataToCSV,
  exportHistoricDataToCSV,
} from "@/lib/csv-export";

// Mapeo de nombres de dimensiones a iconos y colores
const dimensionIcons: Record<string, any> = {
  "emprendimiento e innovación": Lightbulb,
  "capital humano": GraduationCap,
  "ecosistema y colaboración": Users,
  "infraestructura digital": Wifi,
  "servicios públicos digitales": Building2,
  "sostenibilidad digital": Leaf,
  "transformación digital empresarial": Briefcase,
};

const dimensionColors: Record<string, { color: string; bgColor: string }> = {
  "emprendimiento e innovación": { color: "text-primary", bgColor: "bg-primary/10" },
  "capital humano": { color: "text-accent", bgColor: "bg-accent/10" },
  "ecosistema y colaboración": { color: "text-secondary", bgColor: "bg-secondary/10" },
  "infraestructura digital": { color: "text-success", bgColor: "bg-success/10" },
  "servicios públicos digitales": { color: "text-primary", bgColor: "bg-primary/10" },
  "sostenibilidad digital": { color: "text-accent", bgColor: "bg-accent/10" },
  "transformación digital empresarial": { color: "text-secondary", bgColor: "bg-secondary/10" },
};

const KPIsDashboard = () => {
  const [selectedDimension, setSelectedDimension] = useState<string>("");
  const [selectedPais] = useState("España");

  // Obtener dimensiones desde Supabase
  const { data: dimensiones, isLoading: loadingDimensiones } = useQuery({
    queryKey: ["dimensiones"],
    queryFn: getDimensiones,
  });

  // Obtener indicadores de la dimensión seleccionada
  const { data: indicadores, isLoading: loadingIndicadores } = useQuery({
    queryKey: ["indicadores-dimension", selectedDimension],
    queryFn: () => getIndicadoresConDatos(selectedDimension || undefined),
    enabled: !!selectedDimension,
  });

  // Obtener datos por subdimensión para gráficos
  const { data: datosSubdimensiones } = useQuery({
    queryKey: ["datos-subdimensiones", selectedDimension, selectedPais],
    queryFn: () => getDatosPorSubdimension(selectedDimension, selectedPais),
    enabled: !!selectedDimension,
  });

  // Establecer primera dimensión como seleccionada por defecto
  useEffect(() => {
    if (dimensiones && dimensiones.length > 0 && !selectedDimension) {
      setSelectedDimension(dimensiones[0].nombre);
    }
  }, [dimensiones, selectedDimension]);

  const getKPIsByDimension = (dimensionNombre: string): IndicadorConDatos[] => {
    if (!indicadores) return [];
    return indicadores.filter((ind) => ind.dimension === dimensionNombre);
  };

  const getPieChartData = (dimensionKPIs: IndicadorConDatos[]) => {
    const subdimensionCount = dimensionKPIs.reduce((acc, kpi) => {
      const subdim = kpi.subdimension || 'Otros';
      acc[subdim] = (acc[subdim] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return Object.entries(subdimensionCount)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 5); // Top 5 subdimensiones
  };

  // Obtener datos históricos para el gráfico de líneas
  const indicadorParaGrafico = indicadores?.find(
    (ind) => ind.totalResultados && ind.totalResultados > 0
  ) || indicadores?.[0];

  const { data: datosHistoricos } = useQuery({
    queryKey: ["datos-historicos", indicadorParaGrafico?.nombre, selectedPais],
    queryFn: () =>
      indicadorParaGrafico
        ? getDatosHistoricosIndicador(indicadorParaGrafico.nombre, selectedPais, 10)
        : Promise.resolve([]),
    enabled: !!indicadorParaGrafico && !!selectedDimension,
  });

  const getLineChartData = () => {
    if (!datosHistoricos || datosHistoricos.length === 0) {
      return [];
    }

    return datosHistoricos.map((item) => ({
      name: item.periodo.toString(),
      valor: item.valor,
    }));
  };

  const getRadarChartData = (dimensionKPIs: IndicadorConDatos[]) => {
    // Usar datos reales de subdimensiones
    if (datosSubdimensiones && datosSubdimensiones.length > 0) {
      return datosSubdimensiones
        .map((item) => {
          const porcentajeConDatos = item.totalIndicadores > 0
            ? Math.round((item.indicadoresConDatos / item.totalIndicadores) * 100)
            : 0;
          const porcentajeSinDatos = item.totalIndicadores > 0
            ? Math.round(((item.totalIndicadores - item.indicadoresConDatos) / item.totalIndicadores) * 100)
            : 0;
          
          return {
            subdimension:
              item.subdimension.length > 30
                ? item.subdimension.substring(0, 30) + "..."
                : item.subdimension,
            "Cobertura": porcentajeConDatos,
            "Sin datos": porcentajeSinDatos,
            "Total indicadores": item.totalIndicadores,
          };
        })
        .filter((item) => item["Total indicadores"] > 0) // Solo mostrar subdimensiones con indicadores
        .slice(0, 10); // Mostrar hasta 10 subdimensiones
    }

    // Fallback: agrupar por subdimensión
    const subdimensionData = dimensionKPIs.reduce((acc, kpi) => {
      const subdim = kpi.subdimension || "Otros";
      if (!acc[subdim]) {
        acc[subdim] = {
          name: subdim,
          total: 0,
          conDatos: 0,
          altaImportancia: 0,
        };
      }
      acc[subdim].total += 1;
      if (kpi.totalResultados && kpi.totalResultados > 0) {
        acc[subdim].conDatos += 1;
      }
      const importance = kpi.importancia?.toLowerCase() || "";
      if (importance.includes("alta")) {
        acc[subdim].altaImportancia += 1;
      }
      return acc;
    }, {} as Record<string, any>);

    return Object.values(subdimensionData)
      .map((item: any) => {
        const porcentajeConDatos = item.total > 0
          ? Math.round((item.conDatos / item.total) * 100)
          : 0;
        const porcentajeSinDatos = item.total > 0
          ? Math.round(((item.total - item.conDatos) / item.total) * 100)
          : 0;
        
        return {
          subdimension:
            item.name.length > 30 ? item.name.substring(0, 30) + "..." : item.name,
          "Cobertura": porcentajeConDatos,
          "Sin datos": porcentajeSinDatos,
          "Total indicadores": item.total,
        };
      })
      .filter((item: any) => item["Total indicadores"] > 0)
      .slice(0, 10);
  };

  const COLORS = [
    "hsl(var(--primary))",
    "hsl(var(--accent))",
    "hsl(var(--secondary))",
    "hsl(var(--success))",
    "hsl(var(--warning))",
  ];

  const loading = loadingDimensiones || loadingIndicadores;

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <NavigationHeader />
        <div className="pt-16 flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
            <p className="text-muted-foreground">Cargando KPIs desde la base de datos...</p>
          </div>
        </div>
        <FooterSection />
      </div>
    );
  }

  if (!dimensiones || dimensiones.length === 0) {
    return (
      <div className="min-h-screen bg-background">
        <NavigationHeader />
        <div className="pt-16 flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Database className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">No hay dimensiones disponibles</p>
          </div>
        </div>
        <FooterSection />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <NavigationHeader />
      
      <main className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-12 text-center">
            <h1 className="text-4xl font-bold text-foreground mb-4 flex items-center justify-center gap-2">
              <TrendingUp className="h-8 w-8 text-primary" />
              Dashboard completo de KPIs
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Sistema de indicadores del ecosistema digital valenciano organizados por dimensiones
            </p>
          </div>

          {/* Tabs por dimensión */}
          <Tabs value={selectedDimension} onValueChange={setSelectedDimension} className="w-full">
            <TabsList className="w-full justify-start flex-wrap h-auto mb-8 bg-muted/50 p-2">
              {dimensiones.map((dimension) => {
                const Icon = dimensionIcons[dimension.nombre.toLowerCase()] || Database;
                const colors = dimensionColors[dimension.nombre.toLowerCase()] || {
                  color: "text-primary",
                  bgColor: "bg-primary/10",
                };
                return (
                  <TabsTrigger
                    key={dimension.id}
                    value={dimension.nombre}
                    className="text-sm px-4 py-2 flex items-center gap-2"
                  >
                    <Icon className="h-4 w-4" />
                    {dimension.nombre}
                  </TabsTrigger>
                );
              })}
            </TabsList>

            {dimensiones.map((dimension) => {
              const dimensionKPIs = getKPIsByDimension(dimension.nombre);
              const topKPIs = dimensionKPIs.slice(0, 4);
              const Icon = dimensionIcons[dimension.nombre.toLowerCase()] || Database;
              const colors = dimensionColors[dimension.nombre.toLowerCase()] || {
                color: "text-primary",
                bgColor: "bg-primary/10",
              };
              
              return (
                <TabsContent key={dimension.id} value={dimension.nombre} className="space-y-8">
                  {/* Header con estadísticas */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <Card className="p-6 bg-gradient-card border-0">
                      <div className="flex items-center justify-between mb-4">
                        <div className={`p-3 rounded-lg ${colors.bgColor}`}>
                          <Icon className={`h-6 w-6 ${colors.color}`} />
                        </div>
                      </div>
                      <h3 className="text-3xl font-bold text-foreground mb-1">
                        {dimensionKPIs.length}
                      </h3>
                      <p className="text-muted-foreground text-sm">Total indicadores</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        Peso: {dimension.peso}%
                      </p>
                    </Card>

                    {topKPIs.slice(0, 3).map((kpi, idx) => (
                      <Card key={idx} className="p-6 bg-gradient-card border-0 hover:shadow-medium transition-all">
                        <div className="flex items-center justify-between mb-4">
                          <div className={`p-3 rounded-lg ${colors.bgColor}`}>
                            <TrendingUp className={`h-6 w-6 ${colors.color}`} />
                          </div>
                          {kpi.totalResultados && kpi.totalResultados > 0 && (
                            <div className="flex items-center space-x-1 text-success">
                              <ArrowUpRight className="h-4 w-4" />
                              <span className="text-sm font-medium">
                                {kpi.totalResultados} datos
                              </span>
                            </div>
                          )}
                        </div>
                        <h3 className="text-lg font-bold text-foreground mb-1 line-clamp-2">
                          {kpi.nombre}
                        </h3>
                        <p className="text-muted-foreground text-sm">{kpi.subdimension || dimension.nombre}</p>
                        {kpi.ultimoValor !== undefined && (
                          <p className="text-xs text-muted-foreground mt-1">
                            Último valor ({kpi.ultimoPeriodo}): {kpi.ultimoValor.toFixed(2)}
                          </p>
                        )}
                      </Card>
                    ))}
                  </div>

                  {/* Gráficos variados */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Gráfico de tarta - Distribución por tipo */}
                    <Card className="p-8 bg-gradient-card border-0 lg:col-span-2">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-semibold text-foreground flex items-center">
                          <Icon className={`h-5 w-5 mr-2 ${colors.color}`} />
                          Distribución por subdimensión
                        </h3>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => {
                            const pieData = getPieChartData(dimensionKPIs);
                            exportChartDataToCSV(pieData, "distribucion_subdimensiones", dimension.nombre);
                          }}
                        >
                          <Download className="h-4 w-4 mr-2" />
                          Exportar CSV
                        </Button>
                      </div>
                      {getPieChartData(dimensionKPIs).length > 0 ? (
                        <ResponsiveContainer width="100%" height={400}>
                          <PieChart>
                            <Pie
                              data={getPieChartData(dimensionKPIs)}
                              cx="50%"
                              cy="50%"
                              labelLine={false}
                              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                              outerRadius={80}
                              fill="#8884d8"
                              dataKey="value"
                            >
                              {getPieChartData(dimensionKPIs).map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Pie>
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: 'hsl(var(--card))', 
                                border: '1px solid hsl(var(--border))',
                                borderRadius: '8px'
                              }}
                            />
                          </PieChart>
                        </ResponsiveContainer>
                      ) : (
                        <div className="flex items-center justify-center h-[400px]">
                          <p className="text-muted-foreground">No hay datos para mostrar</p>
                        </div>
                      )}
                    </Card>

                    {/* Gráfico de líneas - Evolución */}
                    <Card className="p-6 bg-gradient-card border-0">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-semibold text-foreground flex items-center">
                          <TrendingUp className={`h-5 w-5 mr-2 ${colors.color}`} />
                          Evolución histórica
                        </h3>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => {
                            if (datosHistoricos && indicadorParaGrafico) {
                              exportHistoricDataToCSV(datosHistoricos, indicadorParaGrafico.nombre);
                            }
                          }}
                          disabled={!datosHistoricos || datosHistoricos.length === 0}
                        >
                          <Download className="h-4 w-4 mr-2" />
                          Exportar CSV
                        </Button>
                      </div>
                      {getLineChartData().length > 0 ? (
                        <ResponsiveContainer width="100%" height={250}>
                          <AreaChart data={getLineChartData()}>
                            <defs>
                              <linearGradient id={`color-${dimension.id}`} x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.8}/>
                                <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                              </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                            <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" />
                            <YAxis stroke="hsl(var(--muted-foreground))" />
                            <Tooltip 
                              contentStyle={{ 
                                backgroundColor: 'hsl(var(--card))', 
                                border: '1px solid hsl(var(--border))',
                                borderRadius: '8px'
                              }}
                            />
                            <Area 
                              type="monotone" 
                              dataKey="valor" 
                              stroke="hsl(var(--primary))" 
                              fillOpacity={1} 
                              fill={`url(#color-${dimension.id})`}
                              name={indicadorParaGrafico?.nombre || "Valor"}
                            />
                          </AreaChart>
                        </ResponsiveContainer>
                      ) : (
                        <div className="flex items-center justify-center h-[250px]">
                          <p className="text-muted-foreground text-sm">
                            {indicadorParaGrafico 
                              ? "No hay datos históricos disponibles"
                              : "Selecciona un indicador con datos"}
                          </p>
                        </div>
                      )}
                    </Card>
                  </div>

                  {/* Gráfico de radar */}
                  <Card className="p-6 bg-gradient-card border-0">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-semibold text-foreground flex items-center">
                          <Icon className={`h-5 w-5 mr-2 ${colors.color}`} />
                        Análisis por subdimensión
                      </h3>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => {
                          const radarData = getRadarChartData(dimensionKPIs);
                          exportChartDataToCSV(radarData, "analisis_subdimensiones", dimension.nombre);
                        }}
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Exportar CSV
                      </Button>
                    </div>
                    {getRadarChartData(dimensionKPIs).length > 0 ? (
                      <ResponsiveContainer width="100%" height={450}>
                        <RadarChart data={getRadarChartData(dimensionKPIs)}>
                        <PolarGrid stroke="hsl(var(--muted))" />
                        <PolarAngleAxis 
                          dataKey="subdimension" 
                          tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 11 }}
                          style={{ textTransform: 'capitalize' }}
                        />
                        <PolarRadiusAxis 
                          angle={90} 
                          domain={[0, 100]}
                          tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
                          tickFormatter={(value) => `${value}%`}
                        />
                        <Radar
                          name="Cobertura de datos"
                          dataKey="Cobertura"
                          stroke="hsl(var(--success))"
                          fill="hsl(var(--success))"
                          fillOpacity={0.6}
                          strokeWidth={2}
                        />
                        <Radar
                          name="Sin datos"
                          dataKey="Sin datos"
                          stroke="hsl(var(--destructive))"
                          fill="hsl(var(--destructive))"
                          fillOpacity={0.3}
                          strokeWidth={2}
                        />
                        <Tooltip 
                          contentStyle={{ 
                            backgroundColor: 'hsl(var(--card))', 
                            border: '1px solid hsl(var(--border))',
                            borderRadius: '8px',
                            padding: '8px 12px'
                          }}
                          formatter={(value: any, name: string, props: any) => {
                            if (name === "Cobertura de datos" || name === "Sin datos") {
                              return [`${value}%`, name];
                            }
                            if (name === "Total indicadores") {
                              return [`${value} indicadores`, name];
                            }
                            return [value, name];
                          }}
                        />
                        <Legend 
                          wrapperStyle={{ paddingTop: '20px' }}
                          iconType="circle"
                          formatter={(value) => {
                            if (value === "Cobertura de datos") return "Cobertura";
                            return value;
                          }}
                        />
                      </RadarChart>
                    </ResponsiveContainer>
                    ) : (
                      <div className="flex items-center justify-center h-[450px]">
                        <p className="text-muted-foreground">No hay datos para mostrar</p>
                      </div>
                    )}
                  </Card>

                  {/* Lista con barras de progreso - Solo algunos indicadores */}
                  <Card className="p-6 bg-gradient-card border-0">
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-xl font-semibold text-foreground flex items-center">
                        <Icon className={`h-5 w-5 mr-2 ${colors.color}`} />
                        Indicadores destacados
                      </h3>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => {
                          exportIndicadoresToCSV(dimensionKPIs, dimension.nombre);
                        }}
                        disabled={dimensionKPIs.length === 0}
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Exportar todos
                      </Button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {dimensionKPIs.slice(0, 6).map((kpi, idx) => {
                        const tieneDatos = kpi.totalResultados && kpi.totalResultados > 0;
                        const porcentaje = tieneDatos ? 75 : 30;
                        return (
                          <div key={idx} className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span className="text-foreground font-medium line-clamp-1">
                                {kpi.nombre}
                              </span>
                              <span className="text-muted-foreground">
                                {kpi.importancia || 'N/A'}
                              </span>
                            </div>
                            <Progress value={porcentaje} className="h-2" />
                            {kpi.totalResultados !== undefined && (
                              <p className="text-xs text-muted-foreground">
                                {kpi.totalResultados} resultados disponibles
                              </p>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </Card>

                  {/* Detalles de todos los indicadores */}
                  <div>
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-2xl font-bold text-foreground">
                        Todos los indicadores - {dimension.nombre}
                      </h3>
                      <Button 
                        variant="outline"
                        onClick={() => {
                          exportIndicadoresToCSV(dimensionKPIs, dimension.nombre);
                        }}
                        disabled={dimensionKPIs.length === 0}
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Exportar todos a CSV
                      </Button>
                    </div>
                    {dimensionKPIs.length === 0 ? (
                      <Card className="p-6 bg-muted/50">
                        <p className="text-muted-foreground text-center">
                          No hay indicadores disponibles para esta dimensión
                        </p>
                      </Card>
                    ) : (
                      <div className="grid gap-6">
                        {dimensionKPIs.map((kpi, index) => (
                          <Card key={index} className="p-6 hover:shadow-medium transition-all border-l-4 border-l-primary">
                            <div className="space-y-4">
                              <div className="flex items-start justify-between gap-4">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                                    {kpi.totalResultados && kpi.totalResultados > 0 ? (
                                      <Badge className="bg-success/10 text-success">
                                        Con datos ({kpi.totalResultados})
                                      </Badge>
                                    ) : (
                                      <Badge className="bg-muted text-muted-foreground">
                                        Sin datos
                                      </Badge>
                                    )}
                                    {kpi.importancia && (
                                      <Badge className={
                                        kpi.importancia.toLowerCase().includes('alta') ? "bg-destructive/10 text-destructive" :
                                        kpi.importancia.toLowerCase().includes('media') ? "bg-warning/10 text-warning" :
                                        "bg-success/10 text-success"
                                      }>
                                        {kpi.importancia}
                                      </Badge>
                                    )}
                                    {kpi.origen_indicador && (
                                      <Badge variant="outline" className="text-xs">
                                        {kpi.origen_indicador}
                                      </Badge>
                                    )}
                                  </div>
                                  <h4 className="text-xl font-semibold text-foreground mb-1">
                                    {kpi.nombre}
                                  </h4>
                                  {kpi.subdimension && (
                                    <p className="text-sm text-muted-foreground">
                                      Subdimensión: {kpi.subdimension}
                                    </p>
                                  )}
                                  {kpi.ultimoValor !== undefined && kpi.ultimoPeriodo && (
                                    <p className="text-sm text-foreground mt-2">
                                      Último valor ({kpi.ultimoPeriodo}): <strong>{kpi.ultimoValor.toFixed(2)}</strong>
                                    </p>
                                  )}
                                </div>
                              </div>

                              {kpi.formula && (
                                <div>
                                  <h5 className="text-sm font-semibold text-foreground mb-1">
                                    Fórmula de cálculo
                                  </h5>
                                  <p className="text-sm text-muted-foreground font-mono bg-muted/30 p-2 rounded">
                                    {kpi.formula}
                                  </p>
                                </div>
                              )}

                              <div className="pt-4 border-t flex flex-wrap gap-4 text-xs text-muted-foreground">
                                {kpi.origen_indicador && (
                                  <div>
                                    <span className="font-medium">Origen: </span>
                                    {kpi.origen_indicador}
                                  </div>
                                )}
                                {kpi.fuente && (
                                  <div>
                                    <span className="font-medium">Fuente: </span>
                                    {kpi.fuente}
                                  </div>
                                )}
                              </div>
                            </div>
                          </Card>
                        ))}
                      </div>
                    )}
                  </div>
                </TabsContent>
              );
            })}
          </Tabs>
        </div>
      </main>

      <FooterSection />
    </div>
  );
};

export default KPIsDashboard;
