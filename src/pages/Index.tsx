import NavigationHeader from "@/components/NavigationHeader";
import HeroSection from "@/components/HeroSection";
import DashboardSection from "@/components/DashboardSection";
import DataSourcesSection from "@/components/DataSourcesSection";
import FooterSection from "@/components/FooterSection";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <NavigationHeader />
      <HeroSection />
      <DashboardSection />
      <DataSourcesSection />
      <FooterSection />
    </div>
  );
};

export default Index;
