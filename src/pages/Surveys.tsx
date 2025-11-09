import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { usePermissions } from "@/hooks/usePermissions";
import { FileText, Calendar, Users, Plus } from "lucide-react";
import { toast } from "sonner";
import NavigationHeader from "@/components/NavigationHeader";
import FooterSection from "@/components/FooterSection";

interface Survey {
  id: string;
  title: string;
  description: string | null;
  created_at: string;
  active: boolean;
}

const Surveys = () => {
  const [surveys, setSurveys] = useState<Survey[]>([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const { permissions } = usePermissions();
  const navigate = useNavigate();

  useEffect(() => {
    fetchSurveys();
  }, []);

  const fetchSurveys = async () => {
    try {
      const { data, error } = await supabase
        .from("surveys")
        .select("*")
        .eq("active", true)
        .order("created_at", { ascending: false });

      if (error) throw error;
      setSurveys(data || []);
    } catch (error) {
      console.error("Error fetching surveys:", error);
      toast.error("Error al cargar las encuestas");
    } finally {
      setLoading(false);
    }
  };

  const handleStartSurvey = (surveyId: string) => {
    if (!user) {
      toast.error("Debes iniciar sesión para participar en encuestas");
      navigate("/auth");
      return;
    }
    navigate(`/encuestas/${surveyId}`);
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <NavigationHeader />
      
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 mt-8">
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center gap-4">
              <h1 className="text-4xl md:text-5xl font-bold text-foreground leading-tight">
                Encuestas disponibles
              </h1>
              {permissions.canUploadDataSources && (
                <Button
                  onClick={() => navigate("/encuestas/crear")}
                  size="lg"
                  className="flex items-center gap-2"
                >
                  <Plus className="h-5 w-5" />
                  Crear encuesta
                </Button>
              )}
            </div>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Participa en las encuestas del ecosistema digital valenciano
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <Card key={i} className="animate-pulse">
                  <CardHeader>
                    <div className="h-6 bg-muted rounded w-3/4 mb-2" />
                    <div className="h-4 bg-muted rounded w-full" />
                  </CardHeader>
                  <CardContent>
                    <div className="h-10 bg-muted rounded" />
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : surveys.length === 0 ? (
            <Card className="text-center py-12">
              <CardContent>
                <FileText className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                <p className="text-xl text-muted-foreground">
                  No hay encuestas disponibles en este momento
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {surveys.map((survey) => (
                <Card key={survey.id} className="hover:shadow-lg transition-all duration-300">
                  <CardHeader>
                    <CardTitle className="flex items-start gap-2">
                      <FileText className="h-5 w-5 text-primary mt-1 flex-shrink-0" />
                      <span className="line-clamp-2">{survey.title}</span>
                    </CardTitle>
                    <CardDescription className="line-clamp-3">
                      {survey.description || "Sin descripción"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Calendar className="h-4 w-4" />
                      <span>
                        1 de septiembre
                      </span>
                    </div>
                    <Button
                      onClick={() => handleStartSurvey(survey.id)}
                      className="w-full"
                    >
                      <Users className="mr-2 h-4 w-4" />
                      Participar
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </main>

      <FooterSection />
    </div>
  );
};

export default Surveys;