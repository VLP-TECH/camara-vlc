import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/AuthContext";
import { ArrowLeft, Send } from "lucide-react";
import { toast } from "sonner";
import NavigationHeader from "@/components/NavigationHeader";
import FooterSection from "@/components/FooterSection";

interface Survey {
  id: string;
  title: string;
  description: string | null;
}

interface Question {
  id: string;
  question_text: string;
  question_type: string;
  options: any;
  required: boolean;
  order_index: number;
}

const SurveyForm = () => {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [survey, setSurvey] = useState<Survey | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!user) {
      toast.error("Debes iniciar sesión para responder encuestas");
      navigate("/auth");
      return;
    }
    fetchSurveyData();
  }, [id, user]);

  const fetchSurveyData = async () => {
    try {
      const [surveyResult, questionsResult] = await Promise.all([
        supabase.from("surveys").select("*").eq("id", id).single(),
        supabase
          .from("survey_questions")
          .select("*")
          .eq("survey_id", id)
          .order("order_index", { ascending: true }),
      ]);

      if (surveyResult.error) throw surveyResult.error;
      if (questionsResult.error) throw questionsResult.error;

      setSurvey(surveyResult.data);
      setQuestions(questionsResult.data || []);
    } catch (error) {
      console.error("Error fetching survey:", error);
      toast.error("Error al cargar la encuesta");
      navigate("/encuestas");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate required questions
    const missingRequired = questions.some(
      (q) => q.required && !answers[q.id]
    );
    if (missingRequired) {
      toast.error("Por favor, responde todas las preguntas obligatorias");
      return;
    }

    setSubmitting(true);
    try {
      const { error } = await supabase.from("survey_responses").insert({
        survey_id: id,
        user_id: user!.id,
        answers: answers,
      });

      if (error) {
        if (error.code === "23505") {
          toast.error("Ya has respondido esta encuesta");
        } else {
          throw error;
        }
        return;
      }

      toast.success("Encuesta enviada correctamente");
      navigate("/encuestas");
    } catch (error) {
      console.error("Error submitting survey:", error);
      toast.error("Error al enviar la encuesta");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <NavigationHeader />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
            <p className="text-muted-foreground">Cargando encuesta...</p>
          </div>
        </main>
      </div>
    );
  }

  if (!survey) {
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <NavigationHeader />

      <main className="flex-1 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Button
          variant="ghost"
          onClick={() => navigate("/encuestas")}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Volver a encuestas
        </Button>

        <Card>
          <CardHeader>
            <CardTitle className="text-3xl">{survey.title}</CardTitle>
            {survey.description && (
              <CardDescription className="text-base">
                {survey.description}
              </CardDescription>
            )}
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-8">
              {questions.map((question, index) => (
                <div key={question.id} className="space-y-4">
                  <Label className="text-base font-semibold">
                    {index + 1}. {question.question_text}
                    {question.required && (
                      <span className="text-destructive ml-1">*</span>
                    )}
                  </Label>

                  {question.question_type === "text" && (
                    <Input
                      value={answers[question.id] || ""}
                      onChange={(e) =>
                        setAnswers({ ...answers, [question.id]: e.target.value })
                      }
                      required={question.required}
                      placeholder="Tu respuesta"
                    />
                  )}

                  {question.question_type === "textarea" && (
                    <Textarea
                      value={answers[question.id] || ""}
                      onChange={(e) =>
                        setAnswers({ ...answers, [question.id]: e.target.value })
                      }
                      required={question.required}
                      placeholder="Tu respuesta"
                      rows={4}
                    />
                  )}

                  {question.question_type === "multiple_choice" &&
                    question.options?.options && (
                      <RadioGroup
                        value={answers[question.id] || ""}
                        onValueChange={(value) =>
                          setAnswers({ ...answers, [question.id]: value })
                        }
                        required={question.required}
                      >
                        {question.options.options.map(
                          (option: string, optIndex: number) => (
                            <div
                              key={optIndex}
                              className="flex items-center space-x-2"
                            >
                              <RadioGroupItem
                                value={option}
                                id={`${question.id}-${optIndex}`}
                              />
                              <Label
                                htmlFor={`${question.id}-${optIndex}`}
                                className="font-normal cursor-pointer"
                              >
                                {option}
                              </Label>
                            </div>
                          )
                        )}
                      </RadioGroup>
                    )}
                </div>
              ))}

              <div className="flex gap-4 pt-6">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate("/encuestas")}
                  className="flex-1"
                >
                  Cancelar
                </Button>
                <Button type="submit" disabled={submitting} className="flex-1">
                  <Send className="mr-2 h-4 w-4" />
                  {submitting ? "Enviando..." : "Enviar respuestas"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </main>

      <FooterSection />
    </div>
  );
};

export default SurveyForm;