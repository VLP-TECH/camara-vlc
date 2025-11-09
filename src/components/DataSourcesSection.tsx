import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { usePermissions } from "@/hooks/usePermissions";
import { 
  Database, 
  Globe, 
  BarChart3, 
  Zap, 
  CheckCircle,
  AlertCircle,
  ExternalLink,
  RefreshCw,
  Upload,
  Plus
} from "lucide-react";

const DataSourcesSection = () => {
  const { permissions, loading } = usePermissions();

  if (loading) {
    return (
      <section className="py-20 bg-background">
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
      <section className="py-20 bg-background">
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

  const dataSources = [
    {
      name: "Instituto Nacional de Estadística (INE)",
      type: "Oficial",
      status: "active",
      lastUpdate: "2024-01-15",
      frequency: "Mensual",
      indicators: ["Empresas TIC", "Empleo Digital", "Facturación"],
      icon: BarChart3,
      color: "bg-primary/10 text-primary"
    },
    {
      name: "Eurostat - Digital Economy",
      type: "Europeo",
      status: "active",
      lastUpdate: "2024-01-10",
      frequency: "Trimestral",
      indicators: ["DESI Index", "E-commerce", "Digital Skills"],
      icon: Globe,
      color: "bg-accent/10 text-accent"
    },
    {
      name: "Red.es - Banda Ancha",
      type: "Gubernamental",
      status: "active",
      lastUpdate: "2024-01-12",
      frequency: "Mensual",
      indicators: ["Cobertura Fibra", "Velocidades", "Penetración"],
      icon: Zap,
      color: "bg-success/10 text-success"
    },
    {
      name: "Portal de Datos Abiertos GVA",
      type: "Autonómico",
      status: "maintenance",
      lastUpdate: "2024-01-05",
      frequency: "Semanal",
      indicators: ["Startups", "Inversión", "Innovación"],
      icon: Database,
      color: "bg-secondary/10 text-secondary"
    }
  ];

  const integrationMethods = [
    {
      title: "APIs REST",
      description: "Integración directa con servicios oficiales",
      technologies: ["OAuth 2.0", "JWT", "Rate Limiting"],
      status: "Implementado"
    },
    {
      title: "Web Scraping",
      description: "Extracción automatizada de datos públicos",
      technologies: ["Selenium", "Puppeteer", "Scrapy"],
      status: "En desarrollo"
    },
    {
      title: "ETL Pipelines",
      description: "Procesamiento y normalización de datos",
      technologies: ["Apache Airflow", "Pandas", "SQL"],
      status: "Implementado"
    },
    {
      title: "Real-time Streaming",
      description: "Datos en tiempo real y alertas",
      technologies: ["Apache Kafka", "WebSockets", "Redis"],
      status: "Planificado"
    }
  ];

  return (
    <section id="data" className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="flex flex-col lg:flex-row items-center justify-between mb-6">
            <div className="text-left lg:flex-1">
              <h2 className="text-4xl font-bold text-foreground mb-4">
                Fuentes de Datos e Integración
              </h2>
              <p className="text-xl text-muted-foreground max-w-3xl">
                Infraestructura técnica para la captura, procesamiento y almacenamiento automatizado 
                de datos del ecosistema digital valenciano
              </p>
            </div>
            {permissions.canUploadDataSources && (
              <div className="mt-4 lg:mt-0">
                <Button size="lg" className="mr-2">
                  <Plus className="mr-2 h-5 w-5" />
                  Nueva Fuente
                </Button>
                <Button variant="outline" size="lg">
                  <Upload className="mr-2 h-5 w-5" />
                  Subir Datos
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Data Sources Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {dataSources.map((source) => (
            <Card key={source.name} className="p-6 hover:shadow-medium transition-all duration-300 bg-gradient-card border-0">
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-lg ${source.color}`}>
                  <source.icon className="h-6 w-6" />
                </div>
                <div className="flex items-center space-x-2">
                  {source.status === 'active' ? (
                    <CheckCircle className="h-5 w-5 text-success" />
                  ) : (
                    <AlertCircle className="h-5 w-5 text-warning" />
                  )}
                  <Badge variant={source.status === 'active' ? 'default' : 'secondary'}>
                    {source.status === 'active' ? 'Activo' : 'Mantenimiento'}
                  </Badge>
                </div>
              </div>
              
              <h3 className="text-lg font-semibold text-foreground mb-2">{source.name}</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Tipo: {source.type} • Actualización: {source.frequency}
              </p>
              
              <div className="space-y-2 mb-4">
                <div className="text-xs text-muted-foreground">
                  Última actualización: {new Date(source.lastUpdate).toLocaleDateString('es-ES')}
                </div>
                <div className="flex flex-wrap gap-1">
                  {source.indicators.map((indicator) => (
                    <Badge key={indicator} variant="outline" className="text-xs">
                      {indicator}
                    </Badge>
                  ))}
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <Button variant="ghost" size="sm">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Ver detalles
                </Button>
                {permissions.canUploadDataSources && (
                  <Button variant="outline" size="sm">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Actualizar
                  </Button>
                )}
              </div>
            </Card>
          ))}
        </div>



        {/* Technical Architecture */}
        <Card className="p-8 bg-gradient-card border-0">
          <h3 className="text-2xl font-semibold text-foreground mb-6 text-center">
            Arquitectura Técnica de Datos
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="space-y-4">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
                <Database className="h-8 w-8 text-primary" />
              </div>
              <h4 className="text-lg font-semibold text-foreground">Captura</h4>
              <p className="text-muted-foreground text-sm">
                APIs, Web Scraping, ETL automático desde fuentes oficiales
              </p>
            </div>

            <div className="space-y-4">
              <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto">
                <RefreshCw className="h-8 w-8 text-accent" />
              </div>
              <h4 className="text-lg font-semibold text-foreground">Procesamiento</h4>
              <p className="text-muted-foreground text-sm">
                Normalización, validación y enriquecimiento de datos
              </p>
            </div>

            <div className="space-y-4">
              <div className="w-16 h-16 bg-success/10 rounded-full flex items-center justify-center mx-auto">
                <BarChart3 className="h-8 w-8 text-success" />
              </div>
              <h4 className="text-lg font-semibold text-foreground">Visualización</h4>
              <p className="text-muted-foreground text-sm">
                Dashboards interactivos y informes automatizados
              </p>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
};

export default DataSourcesSection;