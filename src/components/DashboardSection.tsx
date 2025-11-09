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
  Download
} from "lucide-react";

const DashboardSection = () => {
  const { permissions, loading, roles } = usePermissions();
  
  if (loading) {
    return (
      <section className="py-20 bg-muted/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-muted-foreground">Cargando...</p>
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

  const indicators = [
    {
      title: "Índice DESI Valencia",
      value: "68.2",
      change: "+5.3%",
      trend: "up",
      icon: TrendingUp,
      color: "text-success",
      bgColor: "bg-success/10"
    },
    {
      title: "Empresas TIC",
      value: "2,547",
      change: "+12.8%",
      trend: "up",
      icon: Building,
      color: "text-primary",
      bgColor: "bg-primary/10"
    },
    {
      title: "Empleados Sector Digital",
      value: "124,650",
      change: "+8.9%",
      trend: "up",
      icon: Users,
      color: "text-accent",
      bgColor: "bg-accent/10"
    },
    {
      title: "Facturación Digital",
      value: "€8.5B",
      change: "+15.2%",
      trend: "up",
      icon: Euro,
      color: "text-secondary",
      bgColor: "bg-secondary/10"
    }
  ];

  const digitalSkills = [
    { skill: "Competencias Básicas", percentage: 78, color: "bg-success" },
    { skill: "Competencias Avanzadas", percentage: 45, color: "bg-primary" },
    { skill: "Especialistas TIC", percentage: 62, color: "bg-accent" },
    { skill: "Graduados STEM", percentage: 38, color: "bg-secondary" }
  ];

  const connectivity = [
    { metric: "Banda Ancha Fija", percentage: 89, target: 95 },
    { metric: "Fibra Óptica", percentage: 76, target: 85 },
    { metric: "5G Coverage", percentage: 42, target: 70 },
    { metric: "Internet Móvil", percentage: 94, target: 98 }
  ];

  return (
    <section id="dashboard" className="py-20 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-foreground mb-4">
            Dashboard del Ecosistema Digital
          </h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Monitorización en tiempo real de los indicadores clave del desarrollo digital valenciano
          </p>
        </div>

        {/* Key Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {indicators.map((indicator) => (
            <Card key={indicator.title} className="p-6 hover:shadow-medium transition-all duration-300 bg-gradient-card border-0">
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg ${indicator.bgColor}`}>
                  <indicator.icon className={`h-6 w-6 ${indicator.color}`} />
                </div>
                <div className="flex items-center space-x-1 text-success">
                  <ArrowUpRight className="h-4 w-4" />
                  <span className="text-sm font-medium">{indicator.change}</span>
                </div>
              </div>
              <h3 className="text-3xl font-bold text-foreground mb-1">{indicator.value}</h3>
              <p className="text-muted-foreground text-sm">{indicator.title}</p>
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
              {digitalSkills.map((skill) => (
                <div key={skill.skill} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-foreground font-medium">{skill.skill}</span>
                    <span className="text-muted-foreground">{skill.percentage}%</span>
                  </div>
                  <Progress value={skill.percentage} className="h-2" />
                </div>
              ))}
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
              {connectivity.map((item) => (
                <div key={item.metric} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-foreground font-medium">{item.metric}</span>
                    <span className="text-muted-foreground">{item.percentage}% / {item.target}%</span>
                  </div>
                  <div className="relative">
                    <Progress value={(item.percentage / item.target) * 100} className="h-2" />
                    <div 
                      className="absolute top-0 w-1 h-2 bg-warning" 
                      style={{ left: `${(item.target / 100) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
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
                <Button variant="outline" size="sm" className="w-full" onClick={() => window.location.href = '/admin'}>
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