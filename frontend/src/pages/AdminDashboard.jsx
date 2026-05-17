import { ShieldCheck, Siren, TrendingUp, Users } from "lucide-react";

import DataTable from "../components/DataTable";
import MetricCard from "../components/MetricCard";

export default function AdminDashboard() {
  const users = [];
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-black">Admin Dashboard</h1>
        <p className="mt-1 text-slate-500 dark:text-slate-400">Manage users, verify influencers, monitor campaigns, and review platform health.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard icon={Users} label="Users" value="1,284" />
        <MetricCard icon={ShieldCheck} label="Verified" value="342" tone="mint" />
        <MetricCard icon={Siren} label="Risk Accounts" value="18" tone="coral" />
        <MetricCard icon={TrendingUp} label="Campaigns" value="96" />
      </div>
      <DataTable
        columns={[
          { key: "display_name", label: "Influencer" },
          { key: "niche", label: "Niche" },
          { key: "followers", label: "Followers" },
          { key: "engagement_rate", label: "Engagement" },
          { key: "actions", label: "Actions", render: () => <button className="btn-secondary">Verify</button> },
        ]}
        rows={users}
        empty="No platform records loaded yet."
      />
    </div>
  );
}
