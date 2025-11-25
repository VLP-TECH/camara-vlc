import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { usePermissions } from "@/hooks/usePermissions";
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Building, 
  Smartphone, 
  Wifi, 
  GraduationCap,
  Euro,
  ArrowUpRight,
  Download,
  Loader2,
  Database
} from "lucide-react";
import {
  getDashboardStats,
  getLatestIndicatorValues,
  getTopIndicators,
  getIndicatorTrend,
} from "@/lib/dashboard-data";

const DashboardSection = () => {
  const { permissions, loading: permissionsLoading, roles } = usePermissions();
  const [selectedPais] = useState("España");
  
  // Obtener estadísticas del dashboard
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: getDashboardStats,
    refetchInterval: 60000, // Actualizar cada minuto
  });

  // Obtener valores más recientes de indicadores
  const { data: latestValues, isLoading: valuesLoading } = useQuery({
    queryKey: ["latest-indicator-values", selectedPais],
    queryFn: () => getLatestIndicatorValues(selectedPais),
    refetchInterval: 60000,
  });

  // Obtener indicadores más importantes
  const { data: topIndicators, isLoading: topIndicatorsLoading } = useQuery({
    queryKey: ["top-indicators"],
    queryFn: () => getTopIndicators(4),
  });

  // Obtener tendencias de indicadores clave
  const { data: skillsTrend } = useQuery({
    queryKey: ["indicator-trend", "Personas con habilidades digitales básicas", selectedPais],
    queryFn: () => getIndicatorTrend("Personas con habilidades digitales básicas", selectedPais, 5),
    enabled: !!selectedPais,
  });

  const { data: connectivityTrend } = useQuery({
    queryKey: ["indicator-trend", "Adopción de banda ancha fija", selectedPais],
    queryFn: () => getIndicatorTrend("Adopción de banda ancha fija (suscripciones/100 personas)", selectedPais, 5),
    enabled: !!selectedPais,
  });

  const isLoading = permissionsLoading || statsLoading || valuesLoading || topIndicatorsLoading;

  if (isLoading) {
    return (
      <section className="py-20 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
            <p className="text-muted-foreground">Cargando datos del dashboard...</p>
          </div>
        </div>
      </section>
    );
  }

  if (!permissions.canViewData) {
    return (
      <section className="py-20 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-foreground mb-4">
              Acceso Restringido
            </h2>
            <p className="text-muted-foreground">
              Tu cuenta necesita ser activada para ver los datos. Contacta con un administrador.
            </p>
          </div>
        </div>
      </section>
    );
  }

  // Preparar indicadores con datos reales
  const indicators = [
    {
      title: "Total Indicadores",
      value: stats?.totalIndicadores?.toLocaleString() || "0",
      change: "",
      trend: "up" as const,
      icon: Database,
      color: "text-success",
      bgColor: "bg-success/10"
    },
    {
      title: "Total Resultados",
      value: stats?.totalResultados?.toLocaleString() || "0",
      change: "",
      trend: "up" as const,
      icon: TrendingUp,
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      title: "Dimensiones",
      value: stats?.totalDimensiones?.toString() || "0",
      change: "",
      trend: "up" as const,
      icon: Building,
      color: "text-accent",
      bgColor: "bg-accent/10"
    },
    {
      title: "Datos Crudos",
      value: stats?.totalDatosCrudos?.toLocaleString() || "0",
      change: "",
      trend: "up" as const,
      icon: Database,
      color: "text-secondary",
      bgColor: "bg-secondary/10"
    }
  ];

  // Obtener valores reales de indicadores clave si están disponibles
  const habilidadesBasicas = latestValues?.find(
    (v) => v.nombre === "Personas con habilidades digitales básicas"
  );
  const habilidadesAvanzadas = latestValues?.find(
    (v) => v.nombre === "Personas con habilidades digitales generales superiores a las básicas"
  );
  const empresasTIC = latestValues?.find(
    (v) => v.nombre === "Número de empresas que realizan I+D en el sector TIC"
  );
  const bandaAncha = latestValues?.find(
    (v) => v.nombre === "Adopción de banda ancha fija (suscripciones/100 personas)"
  );

  // Preparar datos de competencias digitales con datos reales
  const digitalSkills = [
    { 
      skill: "Competencias Básicas", 
      percentage: habilidadesBasicas ? Math.round(habilidadesBasicas.valor) : 0, 
      color: "bg-success",
      valor: habilidadesBasicas?.valor || 0
    },
    { 
      skill: "Competencias Avanzadas", 
      percentage: habilidadesAvanzadas ? Math.round(habilidadesAvanzadas.valor) : 0, 
      color: "bg-primary",
      valor: habilidadesAvanzadas?.valor || 0
    },
    { 
      skill: "Empresas TIC I+D", 
      percentage: empresasTIC ? Math.min(Math.round(empresasTIC.valor / 10), 100) : 0, 
      color: "bg-accent",
      valor: empresasTIC?.valor || 0
    },
    { 
      skill: "Banda Ancha Fija", 
      percentage: bandaAncha ? Math.round(bandaAncha.valor) : 0, 
      color: "bg-secondary",
      valor: bandaAncha?.valor || 0
    }
  ].filter(skill => skill.percentage > 0 || skill.valor > 0);

  // Preparar datos de conectividad con datos reales
  const connectivity = [
    { 
      metric: "Banda Ancha Fija", 
      percentage: bandaAncha ? Math.round(bandaAncha.valor) : 0, 
      target: 95 
    },
    { 
      metric: "Competencias Básicas", 
      percentage: habilidadesBasicas ? Math.round(habilidadesBasicas.valor) : 0, 
      target: 80 
    },
    { 
      metric: "Competencias Avanzadas", 
      percentage: habilidadesAvanzadas ? Math.round(habilidadesAvanzadas.valor) : 0, 
      target: 60 
    },
    { 
      metric: "Empresas TIC", 
      percentage: empresasTIC ? Math.min(Math.round(empresasTIC.valor / 10), 100) : 0, 
      target: 100 
    }
  ].filter(item => item.percentage > 0);

  return (
    <section id="dashboard" className="py-20 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-foreground mb-4">
            Dashboard del Ecosistema Digital
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-6">
            Monitorización en tiempo real de los indicadores clave del desarrollo digital valenciano
          </p>
          {stats && (
            <div className="flex flex-wrap justify-center gap-4 text-sm text-muted-foreground">
              <span>📊 {stats.totalIndicadores} indicadores</span>
              <span>📈 {stats.totalResultados.toLocaleString()} resultados</span>
              <span>📁 {stats.totalDimensiones} dimensiones</span>
              <span>💾 {stats.totalDatosCrudos.toLocaleString()} datos crudos</span>
            </div>
          )}
        </div>

        {/* Key Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {indicators.map((indicator) => (
            <Card key={indicator.title} className="p-6 hover:shadow-medium transition-all duration-300 bg-gradient-card border-0">
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg ${indicator.bgColor}`}>
                  <indicator.icon className={`h-6 w-6 ${indicator.color}`} />
                </div>
              </div>
              <h3 className="text-3xl font-bold text-foreground mb-1">{indicator.value}</h3>
              <p className="text-muted-foreground text-sm">{indicator.title}</p>
              {indicator.change && (
                <div className="flex items-center space-x-1 text-success mt-2">
                  <ArrowUpRight className="h-4 w-4" />
                  <span className="text-sm font-medium">{indicator.change}</span>
                </div>
              )}
            </Card>
          ))}
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Digital Skills */}
          <Card className="p-6 bg-gradient-card border-0">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-foreground flex items-center">
                <GraduationCap className="h-5 w-5 mr-2 text-primary" />
                Competencias Digitales
              </h3>
              {permissions.canExportData && (
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Exportar
                </Button>
              )}
            </div>
            <div className="space-y-4">
              {digitalSkills.length > 0 ? (
                digitalSkills.map((skill) => (
                  <div key={skill.skill} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-foreground font-medium">{skill.skill}</span>
                      <span className="text-muted-foreground">
                        {skill.percentage}% {skill.valor > 0 && `(${skill.valor.toFixed(1)})`}
                      </span>
                    </div>
                    <Progress value={skill.percentage} className="h-2" />
                  </div>
                ))
              ) : (
                <p className="text-muted-foreground text-sm text-center py-4">
                  No hay datos disponibles de competencias digitales
                </p>
              )}
            </div>
          </Card>

          {/* Connectivity */}
          <Card className="p-6 bg-gradient-card border-0">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-foreground flex items-center">
                <Wifi className="h-5 w-5 mr-2 text-accent" />
                Conectividad Digital
              </h3>
              {permissions.canExportData && (
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Exportar
                </Button>
              )}
            </div>
            <div className="space-y-4">
              {connectivity.length > 0 ? (
                connectivity.map((item) => (
                  <div key={item.metric} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-foreground font-medium">{item.metric}</span>
                      <span className="text-muted-foreground">{item.percentage}% / {item.target}%</span>
                    </div>
                    <div className="relative">
                      <Progress value={Math.min((item.percentage / item.target) * 100, 100)} className="h-2" />
                      <div 
                        className="absolute top-0 w-1 h-2 bg-warning" 
                        style={{ left: `${(item.target / 100) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-muted-foreground text-sm text-center py-4">
                  No hay datos disponibles de conectividad
                </p>
              )}
            </div>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="text-center space-y-4">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="default" size="lg" onClick={() => window.location.href = '/kpis'}>
              <BarChart3 className="mr-2 h-5 w-5" />
              Ver Dashboard Completo
            </Button>
            {permissions.canDownloadReports && (
              <Button variant="outline" size="lg">
                <Download className="mr-2 h-5 w-5" />
                Descargar Informe
              </Button>
            )}
            <Button variant="secondary" size="lg">
              <Smartphone className="mr-2 h-5 w-5" />
              App Móvil
            </Button>
          </div>
          <p className="text-sm text-muted-foreground">
            Datos actualizados automáticamente • Última actualización: {new Date().toLocaleDateString('es-ES')}
          </p>
        </div>

        {/* Admin Panel - Only visible for admins */}
        {roles.isAdmin && (
          <Card className="mt-12 p-6 bg-gradient-to-br from-primary/5 to-accent/5 border-primary/20">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-foreground mb-2 flex items-center justify-center">
                <BarChart3 className="h-6 w-6 mr-2 text-primary" />
                Panel de Control de Administrador
              </h3>
              <p className="text-muted-foreground">
                Funcionalidades avanzadas disponibles para administradores
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="p-4 hover:shadow-lg transition-all">
                <Users className="h-8 w-8 text-primary mb-3" />
                <h4 className="font-semibold text-foreground mb-2">Gestión de Usuarios</h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Administra roles y permisos de usuarios
                </p>
                <Button variant="outline" size="sm" className="w-full" onClick={() => window.location.href = '/admin-usuarios'}>
                  Acceder
                </Button>
              </Card>
              <Card className="p-4 hover:shadow-lg transition-all">
                <Download className="h-8 w-8 text-accent mb-3" />
                <h4 className="font-semibold text-foreground mb-2">Exportación Masiva</h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Exporta todos los datos del sistema
                </p>
                <Button variant="outline" size="sm" className="w-full">
                  Exportar Todo
                </Button>
              </Card>
              <Card className="p-4 hover:shadow-lg transition-all">
                <Building className="h-8 w-8 text-secondary mb-3" />
                <h4 className="font-semibold text-foreground mb-2">Fuentes de Datos</h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Configura y gestiona fuentes de datos
                </p>
                <Button variant="outline" size="sm" className="w-full">
                  Configurar
                </Button>
              </Card>
            </div>
          </Card>
        )}
      </div>
    </section>
  );
};

export default DashboardSection;