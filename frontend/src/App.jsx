import { Route, Routes } from "react-router-dom";

import AppLayout from "./layouts/AppLayout";
import AdminDashboard from "./pages/AdminDashboard";
import AnalyticsPage from "./pages/AnalyticsPage";
import BrandDashboard from "./pages/BrandDashboard";
import CampaignDetails from "./pages/CampaignDetails";
import DiscoveryPage from "./pages/DiscoveryPage";
import HomePage from "./pages/HomePage";
import InfluencerDashboard from "./pages/InfluencerDashboard";
import LoginPage from "./pages/LoginPage";
import MessagingPage from "./pages/MessagingPage";
import FeedPage from "./pages/FeedPage";
import IntegrationsPage from "./pages/IntegrationsPage";
import ProtectedRoute from "./routes/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage mode="login" />} />
        <Route path="/register" element={<LoginPage mode="register" />} />
        <Route element={<ProtectedRoute roles={["BRAND"]} />}>
          <Route path="/brand" element={<BrandDashboard />} />
          <Route path="/discovery" element={<DiscoveryPage />} />
        </Route>
        <Route element={<ProtectedRoute roles={["INFLUENCER"]} />}>
          <Route path="/influencer" element={<InfluencerDashboard />} />
        </Route>
        <Route element={<ProtectedRoute />}>
          <Route path="/feed" element={<FeedPage />} />
          <Route path="/integrations" element={<IntegrationsPage />} />
          <Route path="/campaigns/:id" element={<CampaignDetails />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/messages" element={<MessagingPage />} />
        </Route>
        <Route element={<ProtectedRoute roles={["ADMIN"]} />}>
          <Route path="/admin-dashboard" element={<AdminDashboard />} />
        </Route>
      </Route>
    </Routes>
  );
}
