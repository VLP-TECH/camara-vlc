import { useState, useEffect } from "react";
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
  ArrowUpRight
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
  Legend
} from "recharts";

interface KPI {
  dimension: string;
  subdimension: string;
  indicator: string;
  status: string;
  description: string;
  formula: string;
  data: string;
  source: string;
  importance: string;
  frequency: string;
  sourceDetail: string;
  value?: string;
  change?: string;
}

const dimensions = [
  {
    id: "emprendimiento",
    name: "Apoyo al emprendimiento e innovación",
    icon: Lightbulb,
    color: "text-primary",
    bgColor: "bg-primary/10"
  },
  {
    id: "capital-humano",
    name: "Capital humano",
    icon: GraduationCap,
    color: "text-accent",
    bgColor: "bg-accent/10"
  },
  {
    id: "ecosistema",
    name: "Ecosistema y colaboración",
    icon: Users,
    color: "text-secondary",
    bgColor: "bg-secondary/10"
  },
  {
    id: "infraestructura",
    name: "Infraestructura digital",
    icon: Wifi,
    color: "text-success",
    bgColor: "bg-success/10"
  },
  {
    id: "servicios-publicos",
    name: "Servicios públicos digitales",
    icon: Building2,
    color: "text-primary",
    bgColor: "bg-primary/10"
  },
  {
    id: "sostenibilidad",
    name: "Sostenibilidad digital",
    icon: Leaf,
    color: "text-accent",
    bgColor: "bg-accent/10"
  },
  {
    id: "transformacion",
    name: "Transformación digital empresarial",
    icon: Briefcase,
    color: "text-secondary",
    bgColor: "bg-secondary/10"
  }
];

const KPIsDashboard = () => {
  const [kpis, setKpis] = useState<KPI[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDimension, setSelectedDimension] = useState(dimensions[0].id);

  useEffect(() => {
    loadKPIs();
  }, []);

  const loadKPIs = async () => {
    try {
      const response = await fetch('/data/kpis-completo.csv');
      const text = await response.text();
      const lines = text.split('\n');
      
      const parsedKPIs: KPI[] = [];

      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        const values = line.split(';');
        if (values.length >= 13) {
          const dimensionRaw = values[0]?.trim() || '';
          
          // Mapear dimensiones del CSV a nuestras dimensiones
          let mappedDimension = '';
          const dimLower = dimensionRaw.toLowerCase();
          
          if (dimLower.includes('emprendimiento') || dimLower.includes('innovación') || dimLower.includes('innovacion')) {
            mappedDimension = 'emprendimiento';
          } else if (dimLower.includes('capital') || dimLower.includes('humano')) {
            mappedDimension = 'capital-humano';
          } else if (dimLower.includes('ecosistema') || dimLower.includes('colaboración') || dimLower.includes('colaboracion')) {
            mappedDimension = 'ecosistema';
          } else if (dimLower.includes('infraestructura')) {
            mappedDimension = 'infraestructura';
          } else if (dimLower.includes('servicios') || dimLower.includes('públicos') || dimLower.includes('publicos')) {
            mappedDimension = 'servicios-publicos';
          } else if (dimLower.includes('sostenibilidad')) {
            mappedDimension = 'sostenibilidad';
          } else if (dimLower.includes('transformación') || dimLower.includes('transformacion') || dimLower.includes('empresarial')) {
            mappedDimension = 'transformacion';
          }

          if (mappedDimension) {
            const kpi: KPI = {
              dimension: mappedDimension,
              subdimension: values[1]?.trim() || '',
              indicator: values[2]?.trim() || '',
              status: values[3]?.trim() || '',
              description: values[5]?.trim() || '',
              formula: values[6]?.trim() || '',
              data: values[7]?.trim() || '',
              source: values[8]?.trim() || '',
              importance: values[9]?.trim() || '',
              frequency: values[10]?.trim() || '',
              sourceDetail: values[11]?.trim() || '',
              value: values[7]?.trim() || '',
              change: ''
            };

            parsedKPIs.push(kpi);
          }
        }
      }

      setKpis(parsedKPIs);
      setLoading(false);
    } catch (error) {
      console.error('Error loading KPIs:', error);
      setLoading(false);
    }
  };

  const getKPIsByDimension = (dimensionId: string) => {
    return kpis.filter(kpi => kpi.dimension === dimensionId);
  };

  const getPieChartData = (dimensionKPIs: KPI[]) => {
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

  const getLineChartData = (dimensionKPIs: KPI[]) => {
    const currentYear = new Date().getFullYear();
    return Array.from({ length: 6 }, (_, idx) => ({
      name: `${currentYear - 5 + idx}`,
      inversion: Math.floor(Math.random() * 500) + 200,
    }));
  };

  const COLORS = ['hsl(var(--success))', 'hsl(var(--warning))', 'hsl(var(--destructive))', 'hsl(var(--accent))'];

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <NavigationHeader />
        <div className="pt-16 flex items-center justify-center min-h-[60vh]">
          <p className="text-muted-foreground">Cargando KPIs...</p>
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
              Dashboard Completo de KPIs
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Sistema de indicadores del ecosistema digital valenciano organizados por dimensiones
            </p>
          </div>

          {/* Tabs por dimensión */}
          <Tabs value={selectedDimension} onValueChange={setSelectedDimension} className="w-full">
            <TabsList className="w-full justify-start flex-wrap h-auto mb-8 bg-muted/50 p-2">
              {dimensions.map((dimension) => (
                <TabsTrigger 
                  key={dimension.id} 
                  value={dimension.id}
                  className="text-sm px-4 py-2 flex items-center gap-2"
                >
                  <dimension.icon className="h-4 w-4" />
                  {dimension.name}
                </TabsTrigger>
              ))}
            </TabsList>

            {dimensions.map((dimension) => {
              const dimensionKPIs = getKPIsByDimension(dimension.id);
              const topKPIs = dimensionKPIs.slice(0, 4);
              
              return (
                <TabsContent key={dimension.id} value={dimension.id} className="space-y-8">
                  {/* Header con estadísticas */}
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <Card className="p-6 bg-gradient-card border-0">
                      <div className="flex items-center justify-between mb-4">
                        <div className={`p-3 rounded-lg ${dimension.bgColor}`}>
                          <dimension.icon className={`h-6 w-6 ${dimension.color}`} />
                        </div>
                      </div>
                      <h3 className="text-3xl font-bold text-foreground mb-1">
                        {dimensionKPIs.length}
                      </h3>
                      <p className="text-muted-foreground text-sm">Total Indicadores</p>
                    </Card>

                    {topKPIs.slice(0, 3).map((kpi, idx) => (
                      <Card key={idx} className="p-6 bg-gradient-card border-0 hover:shadow-medium transition-all">
                        <div className="flex items-center justify-between mb-4">
                          <div className={`p-3 rounded-lg ${dimension.bgColor}`}>
                            <TrendingUp className={`h-6 w-6 ${dimension.color}`} />
                          </div>
                          {kpi.status === 'OK' && (
                            <div className="flex items-center space-x-1 text-success">
                              <ArrowUpRight className="h-4 w-4" />
                              <span className="text-sm font-medium">Activo</span>
                            </div>
                          )}
                        </div>
                        <h3 className="text-lg font-bold text-foreground mb-1 line-clamp-2">
                          {kpi.indicator}
                        </h3>
                        <p className="text-muted-foreground text-sm">{kpi.subdimension || dimension.name}</p>
                      </Card>
                    ))}
                  </div>

                  {/* Gráficos variados */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Gráfico de tarta - Distribución por tipo */}
                    <Card className="p-8 bg-gradient-card border-0 lg:col-span-2">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-semibold text-foreground flex items-center">
                          <dimension.icon className={`h-5 w-5 mr-2 ${dimension.color}`} />
                          Distribución por Categoría
                        </h3>
                        <Button variant="outline" size="sm">
                          <Download className="h-4 w-4 mr-2" />
                          Exportar
                        </Button>
                      </div>
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
                    </Card>

                    {/* Gráfico de líneas - Evolución */}
                    <Card className="p-6 bg-gradient-card border-0">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-semibold text-foreground flex items-center">
                          <TrendingUp className={`h-5 w-5 mr-2 ${dimension.color}`} />
                          Volumen de Inversión por Startup
                        </h3>
                        <Button variant="outline" size="sm">
                          <Download className="h-4 w-4 mr-2" />
                          Exportar
                        </Button>
                      </div>
                      <ResponsiveContainer width="100%" height={250}>
                        <AreaChart data={getLineChartData(dimensionKPIs)}>
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
                            dataKey="inversion" 
                            stroke="hsl(var(--primary))" 
                            fillOpacity={1} 
                            fill={`url(#color-${dimension.id})`}
                            name="Inversión (M€)"
                          />
                        </AreaChart>
                      </ResponsiveContainer>
                    </Card>
                  </div>

                  {/* Lista con barras de progreso - Solo algunos indicadores */}
                  <Card className="p-6 bg-gradient-card border-0">
                    <div className="flex items-center justify-between mb-6">
                      <h3 className="text-xl font-semibold text-foreground flex items-center">
                        <dimension.icon className={`h-5 w-5 mr-2 ${dimension.color}`} />
                        Indicadores Destacados
                      </h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {dimensionKPIs.slice(0, 6).map((kpi, idx) => (
                        <div key={idx} className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-foreground font-medium line-clamp-1">
                              {kpi.indicator}
                            </span>
                            <span className="text-muted-foreground">
                              {kpi.importance || 'N/A'}
                            </span>
                          </div>
                          <Progress value={kpi.status === 'OK' ? 75 : 45} className="h-2" />
                        </div>
                      ))}
                    </div>
                  </Card>

                  {/* Detalles de todos los indicadores */}
                  <div>
                    <h3 className="text-2xl font-bold text-foreground mb-6">
                      Todos los Indicadores - {dimension.name}
                    </h3>
                    <div className="grid gap-6">
                      {dimensionKPIs.map((kpi, index) => (
                        <Card key={index} className="p-6 hover:shadow-medium transition-all border-l-4 border-l-primary">
                          <div className="space-y-4">
                            <div className="flex items-start justify-between gap-4">
                              <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2 flex-wrap">
                                  {kpi.status && (
                                    <Badge className={kpi.status === 'OK' ? "bg-success/10 text-success" : "bg-muted text-muted-foreground"}>
                                      {kpi.status}
                                    </Badge>
                                  )}
                                  {kpi.importance && (
                                    <Badge className={
                                      kpi.importance.toLowerCase().includes('alta') ? "bg-destructive/10 text-destructive" :
                                      kpi.importance.toLowerCase().includes('media') ? "bg-warning/10 text-warning" :
                                      "bg-success/10 text-success"
                                    }>
                                      {kpi.importance}
                                    </Badge>
                                  )}
                                  {kpi.frequency && (
                                    <Badge variant="outline" className="text-xs">
                                      {kpi.frequency}
                                    </Badge>
                                  )}
                                </div>
                                <h4 className="text-xl font-semibold text-foreground mb-1">
                                  {kpi.indicator}
                                </h4>
                                {kpi.subdimension && (
                                  <p className="text-sm text-muted-foreground">
                                    Subdimensión: {kpi.subdimension}
                                  </p>
                                )}
                              </div>
                            </div>

                            {kpi.description && (
                              <div>
                                <h5 className="text-sm font-semibold text-foreground mb-1">
                                  Descripción
                                </h5>
                                <p className="text-sm text-muted-foreground">
                                  {kpi.description}
                                </p>
                              </div>
                            )}

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
                              {kpi.source && (
                                <div>
                                  <span className="font-medium">Origen: </span>
                                  {kpi.source}
                                </div>
                              )}
                              {kpi.sourceDetail && (
                                <div>
                                  <span className="font-medium">Fuente: </span>
                                  {kpi.sourceDetail}
                                </div>
                              )}
                            </div>
                          </div>
                        </Card>
                      ))}
                    </div>
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
