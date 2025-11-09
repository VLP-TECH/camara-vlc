import NavigationHeader from "@/components/NavigationHeader";
import DashboardSection from "@/components/DashboardSection";
import DataSourcesSection from "@/components/DataSourcesSection";
import FooterSection from "@/components/FooterSection";

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-background">
      <NavigationHeader />
      <div className="pt-16">
        <DashboardSection />
        <DataSourcesSection />
      </div>
      <FooterSection />
    </div>
  );
};

export default Dashboard;
