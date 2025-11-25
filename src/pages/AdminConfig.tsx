import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';
import { Navigate } from 'react-router-dom';
import { useUserProfile } from '@/hooks/useUserProfile';
import { 
  Database, 
  Upload, 
  Settings, 
  RefreshCw, 
  Play, 
  Activity,
  FileText,
  AlertCircle,
  CheckCircle2
} from 'lucide-react';
import NavigationHeader from '@/components/NavigationHeader';
import FooterSection from '@/components/FooterSection';
import { getDatabaseStats, triggerIngesta, getIngestaStatus, getIngestaLog } from '@/lib/brainnova-admin-api';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const AdminConfig = () => {
  const { profile, loading, isAdmin, isActive } = useUserProfile();
  const queryClient = useQueryClient();
  const { toast } = useToast();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Estadísticas de la base de datos
  const { data: dbStats, isLoading: loadingStats, refetch: refetchStats } = useQuery({
    queryKey: ['database-stats'],
    queryFn: getDatabaseStats,
    refetchInterval: 30000,
    retry: 1,
    retryDelay: 1000,
  });

  // Estado de la ingesta
  const { data: ingestaStatus, refetch: refetchIngestaStatus } = useQuery({
    queryKey: ['ingesta-status'],
    queryFn: getIngestaStatus,
    refetchInterval: 5000,
    retry: 1,
    retryDelay: 1000,
  });

  // Logs de ingesta
  const { data: ingestaLogs } = useQuery({
    queryKey: ['ingesta-logs'],
    queryFn: () => getIngestaLog(50),
    refetchInterval: 10000,
    retry: 1,
    retryDelay: 1000,
  });

  // Mutación para iniciar ingesta
  const { mutate: startIngesta, isPending: startingIngesta } = useMutation({
    mutationFn: triggerIngesta,
    onSuccess: () => {
      toast({
        title: "Éxito",
        description: "Proceso de ingesta iniciado",
      });
      queryClient.invalidateQueries({ queryKey: ['ingesta-status'] });
      queryClient.invalidateQueries({ queryKey: ['ingesta-logs'] });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message || "No se pudo iniciar la ingesta",
        variant: "destructive",
      });
    },
  });

  // Función para subir base de datos
  const handleUploadDatabase = async () => {
    if (!selectedFile) {
      toast({
        title: "Error",
        description: "Por favor selecciona un archivo",
        variant: "destructive",
      });
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${API_BASE_URL}/api/v1/admin/upload-database`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Error al subir la base de datos');
      }

      toast({
        title: "Éxito",
        description: "Base de datos subida correctamente",
      });

      setSelectedFile(null);
      refetchStats();
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "No se pudo subir la base de datos",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Cargando...</p>
        </div>
      </div>
    );
  }

  if (!profile || !isAdmin || !isActive) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen bg-background">
      <NavigationHeader />

      <main className="pt-24 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2 flex items-center gap-2">
              <Settings className="h-8 w-8 text-primary" />
              Administración del backend
            </h1>
            <p className="text-muted-foreground">
              Configura el backend, gestiona la ingesta de datos y sube bases de datos
            </p>
          </div>

          <Tabs defaultValue="configuracion" className="w-full">
            <TabsList className="mb-6">
              <TabsTrigger value="configuracion">Configuración</TabsTrigger>
              <TabsTrigger value="ingesta">Ingesta de datos</TabsTrigger>
              <TabsTrigger value="estadisticas">Estadísticas</TabsTrigger>
            </TabsList>

            {/* Tab: Configuración */}
            <TabsContent value="configuracion" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Database className="h-5 w-5" />
                    Subir base de datos
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="database-file">Archivo de base de datos</Label>
                    <Input
                      id="database-file"
                      type="file"
                      accept=".sql,.db,.dump"
                      onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                    />
                    <p className="text-sm text-muted-foreground">
                      Formatos soportados: .sql, .db, .dump
                    </p>
                  </div>
                  <Button
                    onClick={handleUploadDatabase}
                    disabled={!selectedFile}
                    className="flex items-center gap-2"
                  >
                    <Upload className="h-4 w-4" />
                    Subir base de datos
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="h-5 w-5" />
                    Configuración del backend
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>URL del backend</Label>
                    <Input
                      value={import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}
                      disabled
                      className="bg-muted"
                    />
                    <p className="text-sm text-muted-foreground">
                      Configurado mediante variable de entorno
                    </p>
                  </div>
                  <Button variant="outline" className="flex items-center gap-2">
                    <RefreshCw className="h-4 w-4" />
                    Verificar conexión
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Tab: Ingesta de datos */}
            <TabsContent value="ingesta" className="space-y-6">
              <Card>
                <CardHeader>
                  <div className="flex justify-between items-center">
                    <CardTitle className="flex items-center gap-2">
                      <Activity className="h-5 w-5" />
                      Control de ingesta
                    </CardTitle>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        refetchStats();
                        refetchIngestaStatus();
                      }}
                    >
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Actualizar
                    </Button>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                    <div>
                      <p className="font-medium">Estado de la ingesta</p>
                      <p className="text-sm text-muted-foreground flex items-center gap-2">
                        {ingestaStatus?.status === 'running' ? (
                          <>
                            <Activity className="h-4 w-4 animate-pulse text-primary" />
                            En proceso...
                          </>
                        ) : ingestaStatus?.status === 'completed' ? (
                          <>
                            <CheckCircle2 className="h-4 w-4 text-success" />
                            Completada
                          </>
                        ) : ingestaStatus?.status === 'error' ? (
                          <>
                            <AlertCircle className="h-4 w-4 text-destructive" />
                            Error
                          </>
                        ) : (
                          <>
                            <Activity className="h-4 w-4 text-muted-foreground" />
                            Inactiva
                          </>
                        )}
                      </p>
                    </div>
                    <Button
                      onClick={() => startIngesta()}
                      disabled={startingIngesta || ingestaStatus?.status === 'running'}
                    >
                      {startingIngesta ? (
                        <>
                          <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                          Iniciando...
                        </>
                      ) : (
                        <>
                          <Play className="h-4 w-4 mr-2" />
                          Iniciar ingesta
                        </>
                      )}
                    </Button>
                  </div>

                  {ingestaStatus?.last_run && (
                    <div className="text-sm text-muted-foreground">
                      Última ejecución: {new Date(ingestaStatus.last_run).toLocaleString('es-ES')}
                    </div>
                  )}

                  {ingestaLogs && ingestaLogs.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-2 flex items-center gap-2">
                        <FileText className="h-4 w-4" />
                        Logs recientes
                      </h4>
                      <div className="max-h-64 overflow-y-auto space-y-1 bg-background p-3 rounded border">
                        {ingestaLogs.map((log: any, index: number) => (
                          <div key={index} className="text-xs font-mono text-muted-foreground">
                            <span className="text-muted-foreground/70">
                              {new Date(log.timestamp).toLocaleTimeString('es-ES')}
                            </span>
                            {' '}
                            <span className={log.level === 'error' ? 'text-destructive' : ''}>
                              {log.message}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>

            {/* Tab: Estadísticas */}
            <TabsContent value="estadisticas" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Indicadores</CardTitle>
                    <Database className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {loadingStats ? '...' : dbStats?.total_indicadores || 0}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Resultados</CardTitle>
                    <Activity className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {loadingStats ? '...' : dbStats?.total_resultados || 0}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Datos crudos</CardTitle>
                    <Database className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {loadingStats ? '...' : dbStats?.total_datos_crudos || 0}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Datos macro</CardTitle>
                    <Database className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {loadingStats ? '...' : dbStats?.total_datos_macro || 0}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </main>

      <FooterSection />
    </div>
  );
};

export default AdminConfig;

