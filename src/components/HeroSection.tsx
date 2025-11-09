import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { BarChart3, TrendingUp, Users, Building } from "lucide-react";
import heroImage from "@/assets/valencia-artes.jpg";

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img 
          src="/lovable-uploads/4e3f2d95-6fc0-4490-a937-4cf00f2db14e.png" 
          alt="Centro Histórico de Valencia" 
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-primary/80 via-primary/60 to-secondary/40"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="space-y-8">
          <div className="space-y-4">
            <h1 className="text-5xl md:text-7xl font-bold text-white leading-tight">
              Ecosistema digital
              <span className="block bg-gradient-to-r from-secondary to-accent bg-clip-text text-transparent">
                Comunidad Valenciana
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-white/90 max-w-3xl mx-auto leading-relaxed">
              Plataforma integral para el análisis, monitorización y desarrollo del ecosistema digital valenciano
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              variant="hero" 
              size="lg" 
              className="text-lg px-8 py-4"
              onClick={() => navigate('/dashboard')}
            >
              <BarChart3 className="mr-2 h-5 w-5" />
              Explorar dashboard
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              className="text-lg px-8 py-4 border-white/50 text-primary bg-white/90 hover:bg-white hover:text-primary"
              onClick={() => navigate('/encuestas')}
            >
              <Users className="mr-2 h-5 w-5" />
              Participar en encuesta
            </Button>
          </div>

          {/* Key Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-16">
            <Card className="bg-card/10 backdrop-blur-sm border-white/20 p-6 text-center hover:bg-card/20 transition-all duration-300">
              <Building className="h-8 w-8 text-secondary mx-auto mb-3" />
              <h3 className="text-2xl font-bold text-white">2,500+</h3>
              <p className="text-white/80">Empresas digitales</p>
            </Card>

            <Card className="bg-card/10 backdrop-blur-sm border-white/20 p-6 text-center hover:bg-card/20 transition-all duration-300">
              <Users className="h-8 w-8 text-accent mx-auto mb-3" />
              <h3 className="text-2xl font-bold text-white">125,000+</h3>
              <p className="text-white/80">Profesionales TIC</p>
            </Card>

            <Card className="bg-card/10 backdrop-blur-sm border-white/20 p-6 text-center hover:bg-card/20 transition-all duration-300">
              <TrendingUp className="h-8 w-8 text-success mx-auto mb-3" />
              <h3 className="text-2xl font-bold text-white">15.2%</h3>
              <p className="text-white/80">Crecimiento anual</p>
            </Card>

            <Card className="bg-card/10 backdrop-blur-sm border-white/20 p-6 text-center hover:bg-card/20 transition-all duration-300">
              <BarChart3 className="h-8 w-8 text-warning mx-auto mb-3" />
              <h3 className="text-2xl font-bold text-white">€8.5B</h3>
              <p className="text-white/80">Facturación digital</p>
            </Card>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white/60 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;