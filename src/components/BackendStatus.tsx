import { useQuery } from "@tanstack/react-query";
import { AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import { Card } from "@/components/ui/card";
import { getIndicadoresDisponibles } from "@/lib/brainnova-api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const BackendStatus = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["backend-status"],
    queryFn: async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/indicadores-disponibles`, {
          signal: AbortSignal.timeout(5000), // Timeout de 5 segundos
        });
        // Consideramos el backend disponible si responde (incluso con error 500)
        // Un 500 significa que el servidor está funcionando pero puede haber problemas de datos
        // Un error de conexión (catch) significa que el servidor no está disponible
        return response.status < 600; // Cualquier respuesta HTTP válida (incluye 500)
      } catch {
        return false;
      }
    },
    refetchInterval: 30000, // Verificar cada 30 segundos
    retry: 1,
  });

  if (isLoading) {
    return (
      <Card className="p-3 bg-muted/50 border-0 mb-4">
        <div className="flex items-center gap-2">
          <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
          <span className="text-sm text-muted-foreground">Verificando conexión con backend...</span>
        </div>
      </Card>
    );
  }

  if (error || !data) {
    return (
      <Card className="p-3 bg-destructive/10 border-destructive/20 mb-4">
        <div className="flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-destructive" />
          <div className="flex-1">
            <span className="text-sm font-medium text-foreground">Backend no disponible</span>
            <p className="text-xs text-muted-foreground mt-1">
              El backend debe estar corriendo en: {API_BASE_URL}
            </p>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-3 bg-green-500/10 border-green-500/20 mb-4">
      <div className="flex items-center gap-2">
        <CheckCircle2 className="h-4 w-4 text-green-600" />
        <span className="text-sm text-foreground">Backend conectado</span>
      </div>
    </Card>
  );
};

